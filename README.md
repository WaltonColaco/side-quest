# side-quest
HackED 2026 project

## PDF → Markdown → Structured JSON Pipeline

### Prereqs
- Python 3.9+ on PATH
- Dependencies from `requirements.txt`

### 1) Convert PDFs to Markdown
```
python -m pip install -r requirements.txt
python scripts/pdf_to_md.py --input-dir references --output-dir markdown
```
Outputs one `.md` per PDF in `markdown/`, with page headers and cleaned whitespace.

### 2) Add your OpenAI API key
Create `.env` (already present) and set:
```
OPENAI_API_KEY=sk-...
```

### 3) Extract structured requirements with OpenAI
```
python scripts/extract_md_to_structured.py \
  --markdown-dir markdown \
  --output-dir extracted_information \
  --ground-truth ground_truth_accessibility.json \
  --model gpt-4.1 \
  --env-file .env
```
- Produces `{source}_extracted.json` in `extracted_information/`.
- Use `--dry-run` to write prompts without calling the API.

### 3b) One-liner via bash helper
```
chmod +x scripts/run_extraction.sh
./scripts/run_extraction.sh
```
- Optionally override the model: `MODEL_NAME=gpt-4.1-mini ./scripts/run_extraction.sh`

### 4) Normalize extracted JSON (adds provenance + stable IDs)
```
python scripts/normalize_json.py \
  --input-dir extracted_information \
  --output-dir normalized_information \
  --building-type commercial_interiors \
  --include-pattern ""   # optional substring filter (case-insensitive)
```

### 5) Merge normalized JSON deterministically + capture conflicts
```
python scripts/merge_json.py \
  --input-dir normalized_information \
  --output merged/merged.json \
  --conflicts merged/conflicts.json \
  --doc-priority "leed,standard" \
  --include-pattern ""   # optional substring filter (case-insensitive)
```

### 6) Render concise rubric-style Markdown (includes building type)
```
python scripts/render_doc.py \
  --input merged/merged.json \
  --output reports/commercial_interiors.md \
  --per-category 12 \
  --min-confidence 0.0 \
  --top-n 0
```

### 6b) One-liner for steps 4–6 (normalize → merge → render)
```
chmod +x scripts/run_postprocess.sh
bash scripts/run_postprocess.sh
```
Defaults now target housing: BUILDING_TYPE=housing, OUTPUT_FILE=reports/housing.md.  
Override example for commercial interiors: `BUILDING_TYPE=commercial_interiors OUTPUT_FILE=reports/commercial_interiors.md DOC_PRIORITY="leed,standard" PER_CATEGORY=12 MIN_CONFIDENCE=0.9 TOP_N=40 bash scripts/run_postprocess.sh`
Use `INCLUDE_PATTERN=<substring>` to run the pipeline on a subset of files (case-insensitive filename match).

### 7) Chunk-level vector comparison + DB persistence
- Apply the latest migration (adds chunk embeddings and comparisons tables):
```
sqlite3 db/assessment.db ".read migrations/003_chunk_vectors.sql"
```
- Compare extracted Markdown to the rubric, store embeddings and coverage results:
```
python scripts/compare_md_vectors.py \
  --candidate extracted_output/ilovepdf_merged_organized_smart.md \
  --rubric-housing reports/housing.md \
  --rubric-commercial reports/commercial_interiors.md \
  --db db/assessment.db \
  --model text-embedding-3-small \
  --write-assessment          # optional: also writes projects/assessments rows
```
- To run on all Markdown files in a folder: `python scripts/compare_md_vectors.py --candidate extracted_output`
- Building type is auto-detected (housing if it looks like a personal/home doc; otherwise commercial).
- Rubric weights are prioritised: high-impact accessibility markers (e.g., tactile/contrast/signage/egress cues) get a 3× weight bump before weights are normalised.

### Notes
- Ground truth schema lives in `ground_truth_accessibility.json`; update it to change categories/ids.
- Scripts assume Markdown pages are labeled with `## Page N` (added by the PDF→MD step) to derive page_numbers.


### How to run smart_extract.py
- inside virtual environment
```
pip install -r requirements.txt
```

- run smart_extract.py with <Input> being the .pdf containing images, or .txt/.md file conatining information on the plan. PDF or .txt/.md should be in 
```
python scripts/smart_extract.py --input inputs/<input file in .pdf, .txt, or .md format>
```

