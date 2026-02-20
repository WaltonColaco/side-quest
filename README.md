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

### Notes
- Ground truth schema lives in `ground_truth_accessibility.json`; update it to change categories/ids.
- Scripts assume Markdown pages are labeled with `## Page N` (added by the PDF→MD step) to derive page_numbers.
