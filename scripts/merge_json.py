#!/usr/bin/env python3
"""
Merge normalized JSON records with deterministic rules and conflict tracking.

Usage:
  python scripts/merge_json.py \
    --input-dir normalized_information \
    --output merged/merged.json \
    --conflicts merged/conflicts.json \
    --doc-priority "leed,standard"
"""
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List


def load_records(input_dir: Path) -> List[Dict[str, Any]]:
    records = []
    for path in sorted(input_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        records.append(data)
    if not records:
        raise SystemExit(f"No normalized JSON in {input_dir}")
    return records


def doc_priority_index(filename: str, priorities: List[str]) -> int:
    for i, p in enumerate(priorities):
        if p.lower() in filename.lower():
            return i
    return len(priorities)


def merge_values(a: Dict[str, Any], b: Dict[str, Any]):
    merged = dict(a)
    conflicts = {}
    for k, v in b.items():
        if k not in merged:
            merged[k] = v
        elif merged[k] != v:
            conflicts[k] = [merged[k], v]
            # keep higher (string longer) arbitrarily; could be improved
            merged[k] = merged[k] if len(str(merged[k])) >= len(str(v)) else v
    return merged, conflicts


def merge_requirements(records: List[Dict[str, Any]], priorities: List[str]):
    merged: Dict[str, Any] = {}
    conflicts: List[Dict[str, Any]] = []

    for doc in records:
        filename = doc.get("document", {}).get("filename", "")
        prio = doc_priority_index(filename, priorities)
        for req in doc.get("requirements", []):
            key = req["entity_id"]
            req_copy = dict(req)
            req_copy.setdefault("source_history", []).append({"filename": filename, "priority": prio})

            if key not in merged:
                merged[key] = {**req_copy, "sources": [filename], "priority": prio, "conflict": False, "alternates": []}
                continue

            current = merged[key]
            # choose best by confidence, then priority (lower is better)
            take_new = False
            if req_copy.get("confidence", 0) > current.get("confidence", 0):
                take_new = True
            elif req_copy.get("confidence", 0) == current.get("confidence", 0) and prio < current.get("priority", 99):
                take_new = True

            # merge values and detect conflicts
            value_merge, value_conflicts = merge_values(current.get("values", {}), req_copy.get("values", {}))

            text_conflict = (
                current.get("description") != req_copy.get("description")
                or current.get("label") != req_copy.get("label")
            )

            if take_new:
                alt = {k: current.get(k) for k in req_copy.keys()}
                current.update(req_copy)
                current["alternates"].append(alt)
            else:
                current.setdefault("alternates", []).append(req_copy)

            current["values"] = value_merge
            if value_conflicts or text_conflict:
                current["conflict"] = True
                conflicts.append({
                    "entity_id": key,
                    "field_conflicts": value_conflicts,
                    "text_conflict": text_conflict,
                    "sources": current.get("sources", []) + [filename]
                })

            current.setdefault("sources", []).append(filename)
            current["priority"] = min(current.get("priority", prio), prio)

    return merged, conflicts


def main():
    ap = argparse.ArgumentParser(description="Merge normalized JSON files deterministically")
    ap.add_argument("--input-dir", default="normalized_information", type=Path)
    ap.add_argument("--output", default="merged/merged.json", type=Path)
    ap.add_argument("--conflicts", default="merged/conflicts.json", type=Path)
    ap.add_argument("--doc-priority", default="", help="Comma-separated priority hints (substr match, earlier = higher)")
    args = ap.parse_args()

    priorities = [p.strip() for p in args.doc_priority.split(",") if p.strip()]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.conflicts.parent.mkdir(parents=True, exist_ok=True)

    records = load_records(args.input_dir)
    merged, conflicts = merge_requirements(records, priorities)

    merged_out = {"requirements": list(merged.values())}
    args.output.write_text(json.dumps(merged_out, indent=2), encoding="utf-8")
    args.conflicts.write_text(json.dumps(conflicts, indent=2), encoding="utf-8")

    print(f"Merged {len(records)} files -> {args.output}")
    print(f"Conflicts recorded: {len(conflicts)} -> {args.conflicts}")


if __name__ == "__main__":
    main()
