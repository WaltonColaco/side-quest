#!/usr/bin/env python3
"""
Normalize extracted JSON files for deterministic merge.

Usage:
  python scripts/normalize_json.py \
    --input-dir extracted_information \
    --output-dir normalized_information \
    --building-type commercial_interiors
"""
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List


def snake(s: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in s).strip("_")


def hash_id(*parts: str) -> str:
    h = hashlib.sha1("::".join(parts).encode("utf-8")).hexdigest()[:12]
    return h


def normalize_requirement(req: Dict[str, Any], doc_meta: Dict[str, Any], building_type: str) -> Dict[str, Any]:
    label = (req.get("label") or "").strip()
    desc = (req.get("description") or "").strip()
    category_id = (req.get("category_id") or "").strip()
    req_id = (req.get("id") or "").strip() or snake(label) or "req"

    page_numbers = sorted({int(p) for p in req.get("page_numbers", []) if isinstance(p, (int, float, str)) and str(p).strip().isdigit()})

    values = req.get("values") or {}
    norm_values = {}
    for k, v in values.items():
        norm_values[snake(str(k))] = v if not isinstance(v, str) else v.strip()

    confidence = req.get("confidence")
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    entity_key = f"{category_id}|{label.lower()}" if label else req_id
    entity_id = f"ent_{hash_id(entity_key)}"

    return {
        "requirement_id": req_id,
        "entity_id": entity_id,
        "label": label,
        "description": desc,
        "category_id": category_id,
        "building_type": building_type,
        "evidence": (req.get("evidence") or "").strip(),
        "page_numbers": page_numbers,
        "values": norm_values,
        "confidence": confidence,
        "source": {
            "doc_id": doc_meta["doc_id"],
            "filename": doc_meta["filename"],
            "page_range": page_numbers and f"{page_numbers[0]}-{page_numbers[-1]}" or None,
            "chunk_id": None,
        },
    }


def normalize_file(path: Path, output_dir: Path, building_type: str):
    data = json.loads(path.read_text(encoding="utf-8"))
    doc_meta = data.get("document", {})
    filename = doc_meta.get("source") or path.name
    doc_id = f"doc_{hash_id(filename)}"

    norm_reqs: List[Dict[str, Any]] = []
    for req in data.get("requirements", []):
        norm_reqs.append(normalize_requirement(req, {"doc_id": doc_id, "filename": filename}, building_type))

    output = {
        "document": {
            "doc_id": doc_id,
            "filename": filename,
            "building_type": building_type,
        },
        "requirements": norm_reqs,
    }

    out_path = output_dir / path.name
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Normalized {path.name} -> {out_path}")


def main():
    ap = argparse.ArgumentParser(description="Normalize extracted JSON files")
    ap.add_argument("--input-dir", default="extracted_information", type=Path)
    ap.add_argument("--output-dir", default="normalized_information", type=Path)
    ap.add_argument("--building-type", default="commercial_interiors", help="Building type to stamp into records")
    args = ap.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in args.input_dir.glob("*.json") if p.is_file())
    if not files:
        raise SystemExit(f"No JSON files found in {args.input_dir}")

    for f in files:
        normalize_file(f, args.output_dir, args.building_type)

    print("Done.")


if __name__ == "__main__":
    main()
