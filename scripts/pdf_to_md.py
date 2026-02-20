#!/usr/bin/env python3
import argparse
from pathlib import Path

import fitz  # PyMuPDF


def format_markdown(text: str) -> str:
    """
    Clean markdown output:
    - trim trailing spaces
    - collapse multiple blank lines to a single blank line
    """
    lines = []
    previous_blank = False
    for line in text.splitlines():
        stripped = line.rstrip()
        if stripped == "":
            if not previous_blank:
                lines.append("")
            previous_blank = True
        else:
            lines.append(stripped)
            previous_blank = False
    return "\n".join(lines).strip() + "\n"


def extract_page_markdown(page) -> str:
    """Return markdown if supported; otherwise plain text."""
    try:
        return page.get_text("markdown")
    except Exception:
        # Older PyMuPDF versions may not support "markdown"; fallback to plain text
        return page.get_text()


def pdf_to_markdown(pdf_path: Path, out_dir: Path) -> Path:
    doc = fitz.open(pdf_path)
    parts = []
    for idx, page in enumerate(doc, start=1):
        md = extract_page_markdown(page) or ""
        parts.append(f"## Page {idx}\n\n{md.strip()}")
    doc.close()

    output = out_dir / f"{pdf_path.stem}.md"
    output.write_text(format_markdown("\n\n".join(parts)), encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDFs in a folder to Markdown using PyMuPDF."
    )
    parser.add_argument(
        "--input-dir",
        default="references",
        type=Path,
        help="Folder containing PDFs (default: references)",
    )
    parser.add_argument(
        "--output-dir",
        default="markdown",
        type=Path,
        help="Folder for generated .md files (default: markdown)",
    )
    args = parser.parse_args()

    if not args.input_dir.exists():
        raise SystemExit(f"Input folder not found: {args.input_dir}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(p for p in args.input_dir.glob("*.pdf") if p.is_file())
    if not pdfs:
        raise SystemExit("No PDF files found.")

    for pdf in pdfs:
        out_path = pdf_to_markdown(pdf, args.output_dir)
        print(f"Wrote {out_path}")

    print("Done.")


if __name__ == "__main__":
    main()
