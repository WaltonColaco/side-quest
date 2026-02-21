"""
Smart Accessibility Feature Extractor

- Accepts PDF, image (PNG/JPG/JPEG/WEBP/GIF/BMP/TIFF), or text (.txt/.md) file as input
- PDF: handles text pages, image pages, and mixed pages in a single call
- Image: analysed visually via OpenAI vision
- Text: extracts features directly from content
- Building type (housing / commercial) controls which headers are used
- Headers are parsed in order from reports/housing.md or reports/commercial_interiors.md
- Also extracts location (address / coordinates) for geolocation use
- Outputs a Markdown report to extracted_output/

Usage:
    python scripts/smart_extract.py --input inputs/<file.pdf|file.png|file.txt|...> [--building-type housing|commercial] [--output extracted_output/result.md] [--model gpt-4.1]

If --building-type is omitted, OpenAI will detect it automatically from the document.
"""

import os
import re
import sys
import json
import base64
import argparse
from pathlib import Path

import httpx

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
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif"}
IMAGE_MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".bmp": "image/bmp",
    ".tiff": "image/tiff",
    ".tif": "image/tiff",
}
TEXT_EXTENSIONS = {".txt", ".md"}
VALID_EXTENSIONS = {".pdf"} | IMAGE_EXTENSIONS | TEXT_EXTENSIONS


def is_pdf(file_path: Path) -> bool:
    return file_path.suffix.lower() == ".pdf"


def is_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in IMAGE_EXTENSIONS


def get_mime_type(file_path: Path) -> str:
    return IMAGE_MIME_TYPES.get(file_path.suffix.lower(), "image/jpeg")


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
  "input_type": "<pdf|image|text>",
  "location": {{
    "address": "<full street address if present, or null>",
    "coordinates": {{"lat": <latitude>, "lon": <longitude>}},
    "raw": "<any location text found: city, region, postal code, country, building name, etc. — or null>"
  }},
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
- location: extract any address, street, city, region, postal code, country, GPS coordinates, \
  or building name. Set individual fields to null if not present — never omit the location key.
- coordinates: set to null (not an object) if no lat/lon are found.
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


IMAGE_USER_PROMPT = """\
This is an image file (photograph, scan, or diagram). Analyse it carefully.

- Identify all accessibility features, measurements, labels, signage, and layout elements visible.
- For floor plans or diagrams: identify which accessibility topics are visually present \
(e.g. doors → Door Minimum Width; ramps/level changes → Ramps; signage → Wayfinding Signage; \
counters → Accessible Reception and Counters) and extract only those relevant topics.
- Also extract any location information visible: street address, building name, city, region, \
postal code, GPS coordinates, or any other location identifier.

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
def result_to_md(result: dict, headers: dict = None) -> str:
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

    location = result.get("location") or {}
    address = location.get("address")
    coords = location.get("coordinates")
    raw = location.get("raw")
    if address:
        lines.append(f"- **Address:** {address}")
    elif raw:
        lines.append(f"- **Location:** {raw}")
    if isinstance(coords, dict) and coords.get("lat") is not None:
        lines.append(f"- **Coordinates:** {coords['lat']}, {coords['lon']}")

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
        lines.append("")
        if headers:
            # Build reverse map: requirement label -> category
            req_to_cat = {req: cat for cat, reqs in headers.items() for req in reqs}
            by_cat: dict[str, list] = {}
            for req in not_found:
                cat = req_to_cat.get(req, "other")
                by_cat.setdefault(cat, []).append(req)
            for cat, reqs in by_cat.items():
                lines.append(f"### {cat}")
                for req in reqs:
                    lines.append(f"- {req}")
                lines.append("")
        else:
            for req in not_found:
                lines.append(f"- {req}")
            lines.append("")

    return "\n".join(lines)


# -------- GEOCODING --------
def geocode_google(address: str, api_key: str) -> dict | None:
    """Geocode via Google Maps. Returns {"lat": float, "lon": float} or None."""
    try:
        r = httpx.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={"address": address, "key": api_key},
            timeout=10.0,
        )
        data = r.json()
        if data.get("status") == "OK":
            loc = data["results"][0]["geometry"]["location"]
            return {"lat": loc["lat"], "lon": loc["lng"]}
        print(f"[smart_extract] Google geocoding status: {data.get('status')}", file=sys.stderr)
    except Exception as e:
        print(f"[smart_extract] Google geocoding error: {e}", file=sys.stderr)
    return None


def geocode_nominatim(address: str) -> dict | None:
    """Geocode via OpenStreetMap Nominatim (free, no key). Returns {"lat": float, "lon": float} or None."""
    try:
        r = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": address, "format": "json", "limit": 1},
            headers={"User-Agent": "side-quest-accessibility-extractor"},
            timeout=10.0,
        )
        results = r.json()
        if results:
            return {"lat": float(results[0]["lat"]), "lon": float(results[0]["lon"])}
        print(f"[smart_extract] Nominatim returned no results.", file=sys.stderr)
    except Exception as e:
        print(f"[smart_extract] Nominatim geocoding error: {e}", file=sys.stderr)
    return None


def shorten_query(query: str) -> str:
    """Trim an overly verbose location string to the first two meaningful parts."""
    parts = [p.strip() for p in query.split(",")]
    # Drop duplicate parts (e.g. "Edmonton, Alberta, Canada, Edmonton" → deduplicate)
    seen, deduped = set(), []
    for p in parts:
        if p.lower() not in seen:
            seen.add(p.lower())
            deduped.append(p)
    # Keep at most the first 3 parts to avoid over-specifying the query
    return ", ".join(deduped[:3])


def geocode_address(address: str, api_key: str | None) -> dict | None:
    """Try Google Maps first, fall back to Nominatim if unavailable or failed."""
    if api_key:
        print(f"[smart_extract] Geocoding via Google Maps: {address}", file=sys.stderr)
        result = geocode_google(address, api_key)
        if result:
            return result
        print(f"[smart_extract] Google failed — falling back to Nominatim.", file=sys.stderr)
    else:
        print(f"[smart_extract] No GOOGLE_MAPS_API_KEY — using Nominatim.", file=sys.stderr)

    # Try Nominatim with the full query first, then a shortened version
    result = geocode_nominatim(address)
    if result:
        return result
    short = shorten_query(address)
    if short != address:
        print(f"[smart_extract] Retrying Nominatim with shortened query: {short}", file=sys.stderr)
        return geocode_nominatim(short)
    return None


# -------- API CALLS --------
def detect_building_type(client: OpenAI, input_path: Path, model: str) -> str:
    """Makes a quick first call to detect housing vs commercial. Returns 'housing' or 'commercial'."""
    if is_pdf(input_path):
        b64 = encode_file_b64(input_path)
        content = [
            {"type": "text", "text": DETECT_BUILDING_TYPE_PROMPT},
            {"type": "file", "file": {"filename": input_path.name, "file_data": f"data:application/pdf;base64,{b64}"}},
        ]
    elif is_image(input_path):
        b64 = encode_file_b64(input_path)
        mime = get_mime_type(input_path)
        content = [
            {"type": "text", "text": DETECT_BUILDING_TYPE_PROMPT},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
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


def extract_from_image(client: OpenAI, image_path: Path, system: str, model: str) -> dict:
    b64 = encode_file_b64(image_path)
    mime = get_mime_type(image_path)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": IMAGE_USER_PROMPT},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
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

    if input_path.suffix.lower() not in VALID_EXTENSIONS:
        print(
            f"Error: unsupported file type '{input_path.suffix}'. "
            f"Supported: PDF (.pdf), image ({', '.join(sorted(IMAGE_EXTENSIONS))}), "
            f"or text ({', '.join(sorted(TEXT_EXTENSIONS))})",
            file=sys.stderr,
        )
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
    elif is_image(input_path):
        print(f"[smart_extract] Image input: {input_path.name}", file=sys.stderr)
        result = extract_from_image(client, input_path, system, args.model)
        result["input_type"] = "image"
    else:
        print(f"[smart_extract] Text input: {input_path.name}", file=sys.stderr)
        text = read_text(input_path)
        result = extract_from_text(client, text, system, args.model)
        result["input_type"] = "text"

    result["source_file"] = str(input_path)
    result["building_type"] = building_type
    result["model"] = args.model

    # Resolve location: geocode address → coordinates, or drop address if coordinates came directly
    maps_key = env.get("GOOGLE_MAPS_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")
    location = result.get("location") or {}
    address = location.get("address")
    coords = location.get("coordinates")
    coords_valid = isinstance(coords, dict) and coords.get("lat") is not None

    raw = location.get("raw")

    if coords_valid:
        # Coordinates extracted directly from the document — address not needed
        location["address"] = None
        print(f"[smart_extract] Coordinates extracted directly: {coords['lat']}, {coords['lon']}", file=sys.stderr)
    else:
        # Use address if available, otherwise fall back to raw location text (e.g. building name + city)
        geocode_query = address or raw
        if geocode_query:
            geocoded = geocode_address(geocode_query, maps_key)
            if geocoded:
                location["coordinates"] = geocoded
                print(f"[smart_extract] Coordinates: {geocoded['lat']}, {geocoded['lon']}", file=sys.stderr)
            else:
                print(f"[smart_extract] Geocoding returned no result from any provider.", file=sys.stderr)
        else:
            print(f"[smart_extract] No location info found in document — skipping geocoding.", file=sys.stderr)

    result["location"] = location

    md_content = result_to_md(result, headers=headers)

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
