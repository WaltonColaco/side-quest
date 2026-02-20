#!/usr/bin/env python3
"""
Extract structured accessibility requirements from Markdown files using an OpenAI model.

Outputs one JSON per source Markdown into an output folder, using the ground truth
schema as guidance for categories/field names.

Usage (from repo root):
    python scripts/extract_md_to_structured.py \
        --markdown-dir markdown \
        --output-dir extracted_information \
        --ground-truth ground_truth_accessibility.json \
        --model gpt-4.1 \
        --env-file .env

Set OPENAI_API_KEY in your environment or place it in the env file (default .env).
"""
import argparse
import json
import os
from datetime import date
from pathlib import Path
from textwrap import dedent

from openai import OpenAI


def load_ground_truth(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_env_file(path: Path):
    """Load KEY=VALUE pairs from a .env-style file into os.environ if not already set."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def build_prompt(md_text: str, md_path: Path, ground_truth: dict) -> str:
    categories = []
    for cat in ground_truth.get("categories", []):
        categories.append(
            {
                "id": cat.get("id"),
                "label": cat.get("label"),
                "requirement_ids": [r.get("id") for r in cat.get("requirements", [])],
                "requirement_labels": [r.get("label") for r in cat.get("requirements", [])],
            }
        )

    today = date.today().isoformat()

    return dedent(
        f"""
        You are an accessibility compliance analyst. Extract structured requirements from the provided Markdown.

        RULES
        - Base your extraction only on the provided Markdown text.
        - Align each requirement to the closest category id/label from the reference list below.
        - If a requirement matches an existing reference id, reuse that id; otherwise create a new snake_case id prefixed by the category id (e.g., phys_new_001).
        - Capture supporting evidence as a short quote (<=30 words) from the text.
        - Include page_numbers inferred from '## Page N' headers when mentioned near the evidence.
        - If no requirements are found for a category, omit that category.
        - Return JSON only, no extra text.

        REFERENCE CATEGORIES (id, label, known requirement ids/labels):
        {json.dumps(categories, indent=2)}

        OUTPUT FORMAT (strict JSON):
        {{
          "document": {{
            "source": "{md_path.name}",
            "generated": "{today}"
          }},
          "requirements": [
            {{
              "id": "string",
              "label": "string",
              "description": "string",
              "category_id": "string",
              "evidence": "short quote",
              "page_numbers": [int],
              "values": {{"text": "optional extracted measurements or thresholds"}},
              "confidence": 0.0
            }}
          ]
        }}

        MARKDOWN SOURCE STARTS BELOW
        ---
        {md_text}
        ---
        """
    ).strip()


def call_openai(prompt: str, model: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": "Return only JSON; be concise."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def chunk_markdown(md_text: str, max_chars: int) -> list[str]:
    """Chunk markdown into blocks not exceeding max_chars (by characters)."""
    chunks = []
    current: list[str] = []
    size = 0
    for line in md_text.splitlines():
        line_len = len(line) + 1  # account for newline
        if current and size + line_len > max_chars:
            chunks.append("\n".join(current).strip())
            current = [line]
            size = line_len
        else:
            current.append(line)
            size += line_len
    if current:
        chunks.append("\n".join(current).strip())
    return chunks


def process_file(
    md_path: Path,
    output_dir: Path,
    ground_truth: dict,
    model: str,
    dry_run: bool = False,
    chunk_chars: int = 12000,
):
    text = md_path.read_text(encoding="utf-8")
    chunks = chunk_markdown(text, chunk_chars)

    combined_requirements = []

    for idx, chunk_text in enumerate(chunks, start=1):
        prompt = build_prompt(chunk_text, md_path, ground_truth)

        if dry_run:
            preview_path = output_dir / f"{md_path.stem}_chunk{idx}_prompt.txt"
            preview_path.write_text(prompt, encoding="utf-8")
            print(f"[dry-run] wrote prompt to {preview_path}")
            continue

        result_json = call_openai(prompt, model)
        try:
            data = json.loads(result_json)
            combined_requirements.extend(data.get("requirements", []))
        except Exception as exc:
            error_path = output_dir / f"{md_path.stem}_chunk{idx}_error.txt"
            error_path.write_text(result_json, encoding="utf-8")
            print(f"[warn] chunk {idx} JSON parse failed, saved raw response to {error_path}: {exc}")

    if dry_run:
        return

    output = {
        "document": {
            "source": md_path.name,
            "generated": date.today().isoformat(),
            "chunks_processed": len(chunks),
            "chunk_chars": chunk_chars,
        },
        "requirements": combined_requirements,
    }

    output_path = output_dir / f"{md_path.stem}_extracted.json"
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract structured data from Markdown files via OpenAI")
    parser.add_argument("--markdown-dir", default="markdown", type=Path)
    parser.add_argument("--output-dir", default="extracted_information", type=Path)
    parser.add_argument("--ground-truth", default="ground_truth_accessibility.json", type=Path)
    parser.add_argument("--env-file", default=".env", type=Path, help="Path to .env file containing OPENAI_API_KEY")
    parser.add_argument("--model", default="gpt-4.1", help="OpenAI model name")
    parser.add_argument("--dry-run", action="store_true", help="Do not call API; write prompts for review")
    parser.add_argument("--chunk-chars", type=int, default=12000, help="Max characters per API chunk (rough token proxy)")
    args = parser.parse_args()

    load_env_file(args.env_file)

    if not args.markdown_dir.exists():
        raise SystemExit(f"Markdown dir not found: {args.markdown_dir}")
    if not args.ground_truth.exists():
        raise SystemExit(f"Ground truth file not found: {args.ground_truth}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    ground_truth = load_ground_truth(args.ground_truth)

    md_files = sorted(p for p in args.markdown_dir.glob("*.md") if p.is_file())
    if not md_files:
        raise SystemExit(f"No markdown files in {args.markdown_dir}")

    if not os.getenv("OPENAI_API_KEY") and not args.dry_run:
        raise SystemExit("OPENAI_API_KEY is not set. Use --dry-run to skip API calls.")

    for md_path in md_files:
        process_file(
            md_path,
            args.output_dir,
            ground_truth,
            args.model,
            dry_run=args.dry_run,
            chunk_chars=args.chunk_chars,
        )

    print("Done.")


if __name__ == "__main__":
    main()
