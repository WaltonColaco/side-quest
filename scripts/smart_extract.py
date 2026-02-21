"""
Smart Accessibility Feature Extractor

- Auto-detects input as text or image
- For images: identifies visible header topics first, then extracts only relevant info
- Building type (housing / commercial) controls which headers are used
- Headers are parsed in order from reports/housing.md or reports/commercial_interiors.md
- Outputs structured JSON

Usage:
    python scripts/smart_extract.py --input <file> --building-type housing|commercial [--output out.json] [--model gpt-4.1]
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

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tiff", ".tif"}


# -------- ENV LOADER --------
def load_env(env_path: Path) -> dict:
    """Minimal .env parser — no external dependency needed."""
    env = {}
    if not env_path.exists():
        return env
    with open(env_path, encoding="utf-8") as f:
        for line in f:
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


# -------- INPUT DETECTION --------
def is_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in IMAGE_EXTENSIONS


def read_text(file_path: Path) -> str:
    with open(file_path, encoding="utf-8", errors="replace") as f:
        return f.read()


def encode_image_b64(file_path: Path) -> tuple[str, str]:
    """Returns (base64_string, mime_type)."""
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    mime = mime_map.get(file_path.suffix.lower(), "image/png")
    with open(file_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8"), mime


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
  "input_type": "<text|image>",
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
- For images: first identify which header topics are visually present in the image \
  (e.g. floor plan showing doors → Door Minimum Width; ramps drawn → Ramps), \
  then only extract information relevant to those visible topics.
- values should capture specific numbers, measurements, percentages, or standards mentioned.
- confidence: 1.0 = explicitly stated, 0.7 = strongly implied, 0.5 = possible, 0.3 = uncertain.
"""

TEXT_USER_PROMPT = """\
Extract all accessibility features from the following content.

--- CONTENT START ---
{content}
--- CONTENT END ---

Return only the JSON output, no commentary.
"""

IMAGE_USER_PROMPT = """\
Examine this image carefully.

Step 1 — Identify: Which of the listed accessibility topics/categories are visible or \
inferable from this image? (e.g. if you see doors on a floor plan, Door Minimum Width is relevant; \
if you see ramps or level changes, Ramps is relevant; if you see signage, wayfinding requirements \
are relevant, etc.)

Step 2 — Extract: For each relevant topic you identified, extract all accessibility-related \
information present in the image (labels, dimensions, annotations, symbols, room names, etc.).

Return only the JSON output, no commentary.
"""


# -------- API CALLS --------
def extract_from_text(client: OpenAI, text: str, system: str, model: str) -> dict:
    # Truncate to avoid token limits while keeping meaningful content
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


def extract_from_image(client: OpenAI, image_path: Path, system: str, model: str) -> dict:
    b64, mime = encode_image_b64(image_path)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": IMAGE_USER_PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime};base64,{b64}",
                            "detail": "high",
                        },
                    },
                ],
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    return json.loads(response.choices[0].message.content)


# -------- MAIN --------
def main():
    parser = argparse.ArgumentParser(description="Smart accessibility feature extractor")
    parser.add_argument("--input", required=True, help="Path to input file (text/md/pdf or image)")
    parser.add_argument(
        "--building-type",
        required=True,
        choices=["housing", "commercial"],
        help="Building type — controls which rubric headers are used",
    )
    parser.add_argument("--output", default=None, help="Output JSON path (default: stdout)")
    parser.add_argument("--model", default="gpt-4.1", help="OpenAI model (default: gpt-4.1)")
    args = parser.parse_args()

    # Resolve input path
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

    # Parse headers from the correct rubric md
    md_path = HOUSING_MD if args.building_type == "housing" else COMMERCIAL_MD
    if not md_path.exists():
        print(f"Error: rubric file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    headers = parse_headers_from_md(md_path)
    if not headers:
        print(f"Warning: no headers parsed from {md_path}", file=sys.stderr)

    header_str = headers_to_string(headers)
    system = SYSTEM_PROMPT_TEMPLATE.format(
        building_type=args.building_type,
        header_str=header_str,
    )

    # Detect input type and extract
    if is_image(input_path):
        print(f"[smart_extract] Image input detected: {input_path.name}", file=sys.stderr)
        result = extract_from_image(client, input_path, system, args.model)
        result["input_type"] = "image"
    else:
        print(f"[smart_extract] Text input detected: {input_path.name}", file=sys.stderr)
        text = read_text(input_path)
        result = extract_from_text(client, text, system, args.model)
        result["input_type"] = "text"

    # Stamp metadata
    result["source_file"] = str(input_path)
    result["building_type"] = args.building_type
    result["model"] = args.model

    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json, encoding="utf-8")
        print(f"[smart_extract] Written to: {out_path}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
