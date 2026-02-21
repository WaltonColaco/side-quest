"""
Smart Accessibility Feature Extractor

- Accepts PDF or text file as input
- PDF: handles text pages, image pages, and mixed pages in a single call
- Text: extracts features directly from content
- Building type (housing / commercial) controls which headers are used
- Headers are parsed in order from reports/housing.md or reports/commercial_interiors.md
- Outputs a Markdown report to extracted_output/

Usage:
    python scripts/smart_extract.py --input <file.pdf|file.txt|file.md> [--building-type housing|commercial] [--output extracted_output/result.md] [--model gpt-4.1]

If --building-type is omitted, OpenAI will detect it automatically from the document.
"""

import os
import re
import sys
import json
import base64
import argparse
from pathlib import Path

from openai import OpenAI

# -------- PATHS --------
ROOT = Path(__file__).parent.parent
REPORTS_DIR = ROOT / "reports"
HOUSING_MD = REPORTS_DIR / "housing.md"
COMMERCIAL_MD = REPORTS_DIR / "commercial_interiors.md"
ENV_FILE = ROOT / ".env"
OUTPUT_DIR = ROOT / "extracted_output"


# -------- ENV LOADER --------
def load_env(env_path: Path) -> dict:
    """Minimal .env parser — no external dependency needed."""
    env = {}
    if not env_path.exists():
        return env
    lines = None
    for encoding in ("utf-8-sig", "utf-16", "utf-8", "latin-1"):
        try:
            with open(env_path, encoding=encoding) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    if lines is None:
        return env
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


# -------- PARSE MD HEADERS --------
def parse_headers_from_md(md_path: Path) -> dict:
    """
    Returns ordered dict: { category_name: [requirement_label, ...] }
    Reads ## headings as categories and **bold** bullet items as requirements.
    """
    categories = {}
    current_cat = None
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("## "):
                current_cat = line[3:].strip()
                categories[current_cat] = []
            elif current_cat and line.strip().startswith("- **"):
                match = re.match(r"-\s+\*\*(.+?)\*\*", line.strip())
                if match:
                    categories[current_cat].append(match.group(1))
    return categories


def headers_to_string(headers: dict) -> str:
    lines = []
    for cat, reqs in headers.items():
        lines.append(f"\nCategory: {cat}")
        for r in reqs:
            lines.append(f"  - {r}")
    return "\n".join(lines)


# -------- FILE HELPERS --------
def is_pdf(file_path: Path) -> bool:
    return file_path.suffix.lower() == ".pdf"


def read_text(file_path: Path) -> str:
    with open(file_path, encoding="utf-8", errors="replace") as f:
        return f.read()


def encode_file_b64(file_path: Path) -> str:
    with open(file_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


# -------- PROMPTS --------
SYSTEM_PROMPT_TEMPLATE = """\
You are an expert accessibility compliance analyst for {building_type} buildings.

Your job is to extract accessibility-related features from the provided content and map them \
to the categories and requirements listed below. Only include requirements that are genuinely \
present or inferable from the content — do not fabricate data.

Ordered categories and requirements to look for:
{header_str}

Output ONLY a valid JSON object with this exact structure:
{{
  "building_type": "{building_type}",
  "input_type": "<pdf|text>",
  "extracted": [
    {{
      "category": "<category name from list>",
      "requirement": "<requirement label from list>",
      "found": true,
      "description": "<what was found and where>",
      "values": {{ "<key>": "<value>" }},
      "confidence": <0.0-1.0>
    }}
  ],
  "not_found": ["<requirement label>", ...],
  "notes": "<general observations about the content>"
}}

Rules:
- List every requirement that IS found in "extracted" (found: true).
- List requirement labels NOT found in "not_found".
- For diagram/floor plan pages: identify which header topics are visually present \
  (e.g. doors drawn → Door Minimum Width, ramps drawn → Ramps, signage → Wayfinding Signage) \
  and only extract info relevant to those visible topics.
- For text pages: extract all requirements, measurements, and standards mentioned.
- values should capture specific numbers, measurements, percentages, or standards mentioned.
- confidence: 1.0 = explicitly stated, 0.7 = strongly implied, 0.5 = possible, 0.3 = uncertain.
"""

PDF_USER_PROMPT = """\
This is a PDF document. Read every page carefully.

For pages containing diagrams, floor plans, or images:
  - First identify which accessibility topics are visually present \
(e.g. doors on a plan → Door Minimum Width; ramps or level changes → Ramps; \
signage visible → Wayfinding Signage; counters drawn → Accessible Reception and Counters).
  - Then extract only information relevant to those identified topics.

For pages containing readable text:
  - Extract all accessibility-related requirements, measurements, and standards mentioned.

Return only the JSON output, no commentary.
"""

TEXT_USER_PROMPT = """\
Extract all accessibility features from the following text content.

--- CONTENT START ---
{content}
--- CONTENT END ---

Return only the JSON output, no commentary.
"""


DETECT_BUILDING_TYPE_PROMPT = """\
Look at this document and determine whether it relates to a HOUSING (residential) building \
or a COMMERCIAL (office, retail, public, institutional) building.

Clues to look for:
- Housing: bedrooms, kitchens, bathrooms, residential units, dwelling, apartment, house
- Commercial: office, lobby, reception, retail, meeting rooms, assembly, public corridor

Return ONLY a JSON object with this exact structure:
{
  "building_type": "housing" or "commercial",
  "reasoning": "<one sentence explaining why>"
}
"""


# -------- MARKDOWN RENDERER --------
def result_to_md(result: dict) -> str:
    lines = []
    source = Path(result.get("source_file", "unknown")).name
    building = result.get("building_type", "unknown")
    input_type = result.get("input_type", "unknown")
    model = result.get("model", "unknown")

    lines.append(f"# Accessibility Extraction Report")
    lines.append(f"")
    lines.append(f"- **Source:** `{source}`")
    lines.append(f"- **Building type:** {building}")
    lines.append(f"- **Input type:** {input_type}")
    lines.append(f"- **Model:** {model}")
    lines.append(f"")

    notes = result.get("notes", "").strip()
    if notes:
        lines.append(f"## Notes")
        lines.append(notes)
        lines.append("")

    extracted = result.get("extracted", [])
    if extracted:
        # Group by category
        by_cat: dict[str, list] = {}
        for item in extracted:
            cat = item.get("category", "uncategorised")
            by_cat.setdefault(cat, []).append(item)

        lines.append("## Found Requirements")
        lines.append("")
        for cat, items in by_cat.items():
            lines.append(f"### {cat}")
            for item in items:
                conf = item.get("confidence", 0)
                conf_pct = f"{int(conf * 100)}%"
                lines.append(f"- **{item.get('requirement', '?')}** (confidence: {conf_pct})")
                desc = item.get("description", "").strip()
                if desc:
                    lines.append(f"  - {desc}")
                values = item.get("values", {})
                if values:
                    for k, v in values.items():
                        lines.append(f"  - `{k}`: {v}")
            lines.append("")

    not_found = result.get("not_found", [])
    if not_found:
        lines.append("## Not Found")
        for req in not_found:
            lines.append(f"- {req}")
        lines.append("")

    return "\n".join(lines)


# -------- API CALLS --------
def detect_building_type(client: OpenAI, input_path: Path, model: str) -> str:
    """Makes a quick first call to detect housing vs commercial. Returns 'housing' or 'commercial'."""
    if is_pdf(input_path):
        b64 = encode_file_b64(input_path)
        content = [
            {"type": "text", "text": DETECT_BUILDING_TYPE_PROMPT},
            {"type": "file", "file": {"filename": input_path.name, "file_data": f"data:application/pdf;base64,{b64}"}},
        ]
    else:
        text = read_text(input_path)[:6000]
        content = DETECT_BUILDING_TYPE_PROMPT + f"\n\n--- DOCUMENT ---\n{text}"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": content}],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    data = json.loads(response.choices[0].message.content)
    detected = data.get("building_type", "commercial").lower()
    reasoning = data.get("reasoning", "")
    if detected not in ("housing", "commercial"):
        detected = "commercial"
    print(f"[smart_extract] Detected building type: {detected} — {reasoning}", file=sys.stderr)
    return detected


def extract_from_pdf(client: OpenAI, pdf_path: Path, system: str, model: str) -> dict:
    b64 = encode_file_b64(pdf_path)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PDF_USER_PROMPT},
                    {
                        "type": "file",
                        "file": {
                            "filename": pdf_path.name,
                            "file_data": f"data:application/pdf;base64,{b64}",
                        },
                    },
                ],
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return json.loads(response.choices[0].message.content)


def extract_from_text(client: OpenAI, text: str, system: str, model: str) -> dict:
    truncated = text[:15000] if len(text) > 15000 else text
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": TEXT_USER_PROMPT.format(content=truncated)},
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return json.loads(response.choices[0].message.content)


# -------- MAIN --------
def main():
    parser = argparse.ArgumentParser(description="Smart accessibility feature extractor")
    parser.add_argument("--input", required=True, help="Path to input file (.pdf or text file)")
    parser.add_argument(
        "--building-type",
        required=False,
        default=None,
        choices=["housing", "commercial"],
        help="Building type — if omitted, auto-detected from the document by OpenAI",
    )
    parser.add_argument("--output", default=None, help="Output .md path (default: extracted_output/<input_stem>_smart.md)")
    parser.add_argument("--model", default="gpt-4.1", help="OpenAI model (default: gpt-4.1)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Load API key
    env = load_env(ENV_FILE)
    api_key = env.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env or environment.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # Auto-detect building type if not provided
    if args.building_type:
        building_type = args.building_type
        print(f"[smart_extract] Building type: {building_type} (user specified)", file=sys.stderr)
    else:
        print(f"[smart_extract] No building type specified — detecting from document...", file=sys.stderr)
        building_type = detect_building_type(client, input_path, args.model)

    # Parse headers from the correct rubric md
    md_path = HOUSING_MD if building_type == "housing" else COMMERCIAL_MD
    if not md_path.exists():
        print(f"Error: rubric file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    headers = parse_headers_from_md(md_path)
    if not headers:
        print(f"Warning: no headers parsed from {md_path}", file=sys.stderr)

    header_str = headers_to_string(headers)
    system = SYSTEM_PROMPT_TEMPLATE.format(
        building_type=building_type,
        header_str=header_str,
    )

    # Detect input type and extract
    if is_pdf(input_path):
        print(f"[smart_extract] PDF input: {input_path.name}", file=sys.stderr)
        result = extract_from_pdf(client, input_path, system, args.model)
        result["input_type"] = "pdf"
    else:
        print(f"[smart_extract] Text input: {input_path.name}", file=sys.stderr)
        text = read_text(input_path)
        result = extract_from_text(client, text, system, args.model)
        result["input_type"] = "text"

    result["source_file"] = str(input_path)
    result["building_type"] = building_type
    result["model"] = args.model

    md_content = result_to_md(result)

    if args.output:
        out_path = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / f"{input_path.stem}_smart.md"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md_content, encoding="utf-8")
    print(f"[smart_extract] Written to: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
