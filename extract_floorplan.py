"""
Smart PDF Extractor

- Detects structured text pages
- Runs OCR only when necessary
- Extracts ALL possible information
- Outputs a single combined Markdown file
"""

import os
import re
import cv2
import numpy as np
import pytesseract
import pdfplumber
from pdf2image import convert_from_path

# -------- CONFIG --------
PDF_PATH = "images/ilovepdf_merged_organized.pdf"
OUTPUT_DIR = "extracted_output"
OUTPUT_MD = os.path.join(OUTPUT_DIR, "extracted.md")
DPI = 300
TEXT_LENGTH_THRESHOLD = 40
CONF_THRESHOLD = 50

# If Windows:
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
POPPLER_PATH = r"C:/Users/walto/Desktop/Poppler/poppler-25.12.0/Library/bin"  # adjust if you extracted elsewhere

os.makedirs(OUTPUT_DIR, exist_ok=True)


# -------- HELPERS --------

def has_structured_text(page):
    text = page.extract_text()
    return text and len(text.strip()) > TEXT_LENGTH_THRESHOLD


def preprocess_for_ocr(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresh


def extract_text_blocks(image):
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    blocks = []

    for i in range(len(data["text"])):
        if int(data["conf"][i]) > CONF_THRESHOLD and data["text"][i].strip():
            blocks.append({
                "text": data["text"][i],
                "bbox": {
                    "x": data["left"][i],
                    "y": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i]
                }
            })
    return blocks


def extract_numbers(text):
    return re.findall(r"\d+[\'\"\-]?\d*", text)


def extract_dimensions(text):
    return re.findall(r"\d+'\-\d+\"?\s*[xX]\s*\d+'\-\d+\"?", text)


def detect_lines(image):
    edges = cv2.Canny(image, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100,
                            minLineLength=50, maxLineGap=10)

    line_data = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            line_data.append({
                "start": [int(x1), int(y1)],
                "end": [int(x2), int(y2)]
            })
    return line_data


def detect_contours(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contour_data = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        contour_data.append({
            "bbox": [int(x), int(y), int(w), int(h)]
        })
    return contour_data


# -------- MARKDOWN FORMATTER --------

def page_to_md(page_num, is_structured, raw_text, text_blocks, numbers, dimensions, lines, contours):
    lines_md = [f"## Page {page_num}"]

    if is_structured:
        lines_md.append("**Source:** Structured text (no OCR needed)\n")
    else:
        lines_md.append("**Source:** OCR (image-based page)\n")

    # Raw text
    if raw_text and raw_text.strip():
        lines_md.append("### Text Content")
        lines_md.append(raw_text.strip())
        lines_md.append("")

    # Dimensions
    if dimensions:
        lines_md.append("### Dimensions Found")
        for d in dimensions:
            lines_md.append(f"- `{d}`")
        lines_md.append("")

    # Numbers
    if numbers:
        lines_md.append("### Numbers Found")
        lines_md.append(", ".join(f"`{n}`" for n in numbers))
        lines_md.append("")

    # OCR text blocks (image pages only)
    if text_blocks:
        lines_md.append("### OCR Text Blocks")
        for b in text_blocks:
            bbox = b["bbox"]
            lines_md.append(
                f"- `{b['text']}` &nbsp; _(x:{bbox['x']} y:{bbox['y']} w:{bbox['width']} h:{bbox['height']})_"
            )
        lines_md.append("")

    # Detected lines summary
    if lines:
        lines_md.append("### Detected Lines")
        lines_md.append(f"{len(lines)} structural lines detected.")
        lines_md.append("")

    # Detected contours summary
    if contours:
        lines_md.append("### Detected Contours (Shapes)")
        lines_md.append(f"{len(contours)} shapes/regions detected.")
        lines_md.append("")

    lines_md.append("---")
    return "\n".join(lines_md)


# -------- MAIN --------

with pdfplumber.open(PDF_PATH) as pdf:
    images = convert_from_path(PDF_PATH, dpi=DPI, poppler_path=POPPLER_PATH)
    total_pages = len(pdf.pages)
    md_sections = [f"# Extracted Floorplan Data\n\n**Source:** `{PDF_PATH}`  \n**Pages:** {total_pages}\n\n---\n"]

    for page_num, page in enumerate(pdf.pages):
        print(f"Processing Page {page_num + 1}/{total_pages}")

        is_structured = False
        raw_text = ""
        text_blocks = []
        numbers = []
        dimensions = []
        detected_lines = []
        contours = []

        if has_structured_text(page):
            print("  ✔ Structured text detected")
            raw_text = page.extract_text()
            is_structured = True
            numbers = extract_numbers(raw_text)
            dimensions = extract_dimensions(raw_text)

        else:
            print("  ⚠ No structured text — running OCR")
            img = np.array(images[page_num])
            processed = preprocess_for_ocr(img)

            raw_text = pytesseract.image_to_string(processed)
            text_blocks = extract_text_blocks(processed)
            numbers = extract_numbers(raw_text)
            dimensions = extract_dimensions(raw_text)
            detected_lines = detect_lines(img)
            contours = detect_contours(img)

        md_sections.append(page_to_md(
            page_num + 1, is_structured, raw_text,
            text_blocks, numbers, dimensions, detected_lines, contours
        ))

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write("\n\n".join(md_sections))

print(f"\nExtraction complete. Output: {OUTPUT_MD}")