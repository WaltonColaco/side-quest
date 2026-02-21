#!/usr/bin/env python3
"""
Chunk-level Markdown vector comparison against rubric and persistence to SQLite.

- Splits Markdown into logical chunks (headings, bullet groups, tables, paragraph blocks).
- Detects building type (housing vs commercial) and selects the correct rubric file.
- Embeds chunks with OpenAI embeddings (default: text-embedding-3-small).
- Runs coverage comparison (rubric -> candidate) with cosine similarity thresholds:
    strong >= 0.85, partial >= 0.70, otherwise missing.
- Normalizes to a rubric-style score: strong = 1.0, partial = 0.5, missing = 0.0.
- Saves documents, chunks, comparisons, and chunk_matches into SQLite.

Usage:
  python scripts/compare_md_vectors.py \
      --candidate extracted_output/ilovepdf_merged_organized_smart.md \
      --rubric-housing reports/housing.md \
      --rubric-commercial reports/commercial_interiors.md \
      --db db/assessment.db \
      --model text-embedding-3-small

Optional:
  --candidate extracted_output            # process all .md files in the directory
  --write-assessment                      # also write/overwrite a project+assessment summary
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from openai import OpenAI

# ---------- PATHS ----------
ROOT = Path(__file__).parent.parent
DEFAULT_DB = ROOT / "db" / "assessment.db"
DEFAULT_ENV = ROOT / ".env"
DEFAULT_RUBRIC_HOUSING = ROOT / "reports" / "housing.md"
DEFAULT_RUBRIC_COMMERCIAL = ROOT / "reports" / "commercial_interiors.md"

STRONG_THRESHOLD = 0.80
PARTIAL_THRESHOLD = 0.60


# ---------- DATA CLASSES ----------
@dataclass
class Chunk:
    idx: int
    label: str
    heading_level: int
    path: str
    text: str
    clean_text: str
    embedding: List[float] | None = None
    db_id: int | None = None


# ---------- HELPERS ----------
def load_env(env_path: Path) -> dict:
    env = {}
    if not env_path.exists():
        return env
    for enc in ("utf-8-sig", "utf-16", "utf-8", "latin-1"):
        try:
            lines = env_path.read_text(encoding=enc).splitlines()
            break
        except UnicodeError:
            lines = None
    if not lines:
        return env
    for line in lines:
        if "=" not in line or line.strip().startswith("#"):
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def strip_markdown(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)          # images
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)       # links -> text
    text = re.sub(r"`{1,3}.*?`", " ", text)                    # inline code
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)               # bold
    text = re.sub(r"\*(.*?)\*", r"\1", text)                   # italics
    text = re.sub(r"^>+\s?", "", text, flags=re.MULTILINE)     # blockquote markers
    text = re.sub(r"#\s*", "", text)                           # heading markers
    return " ".join(text.split())


def detect_building_type(md_text: str) -> str:
    meta_match = re.search(r"building type:\s*([A-Za-z]+)", md_text, flags=re.I)
    if meta_match:
        candidate = meta_match.group(1).lower()
        if candidate in ("housing", "residential", "home", "personal"):
            return "housing"
        if candidate == "commercial":
            return "commercial"

    housing_hits = re.findall(r"\b(home|house|apartment|bedroom|kitchen|dwelling|suite)\b", md_text, flags=re.I)
    commercial_hits = re.findall(r"\b(office|lobby|retail|meeting|assembly|theatre|tenant|mall|library)\b", md_text, flags=re.I)
    if len(housing_hits) >= len(commercial_hits):
        return "housing"
    return "commercial"


def chunk_markdown(md_text: str, doc_label: str) -> List[Chunk]:
    lines = md_text.splitlines()
    chunks: List[Chunk] = []
    buf: List[str] = []
    heading_stack: List[Tuple[int, str]] = []
    chunk_idx = 0
    current_kind = None

    def current_path() -> str:
        if not heading_stack:
            return "root"
        return " > ".join([h for _, h in heading_stack])

    def flush(label_hint: str | None = None):
        nonlocal buf, chunk_idx
        text = "\n".join(buf).strip()
        if not text:
            buf = []
            return
        label = label_hint or (heading_stack[-1][1] if heading_stack else "body")
        chunks.append(
            Chunk(
                idx=chunk_idx,
                label=label,
                heading_level=heading_stack[-1][0] if heading_stack else 0,
                path=current_path(),
                text=text,
                clean_text=strip_markdown(text),
            )
        )
        chunk_idx += 1
        buf = []

    heading_re = re.compile(r"^(#{1,6})\s+(.*)$")
    table_re = re.compile(r"^\s*\|.*\|\s*$")
    list_re = re.compile(r"^\s*([-*+]|[0-9]+\.)\s+")

    for line in lines:
        if not line.strip():
            flush()
            current_kind = None
            continue

        h_match = heading_re.match(line)
        if h_match:
            flush()
            level = len(h_match.group(1))
            title = h_match.group(2).strip()
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
            current_kind = "heading"
            continue

        kind = "table" if table_re.match(line) else "list" if list_re.match(line) else "text"
        if current_kind and kind != current_kind:
            flush()
        current_kind = kind
        buf.append(line)

    flush()
    return chunks


def embed_chunks(client: OpenAI, model: str, chunks: List[Chunk], batch_size: int = 64) -> None:
    texts = [c.clean_text for c in chunks]
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        resp = client.embeddings.create(model=model, input=batch)
        for offset, data in enumerate(resp.data):
            chunks[start + offset].embedding = data.embedding


def cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def ensure_schema(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS documents (
          id             INTEGER PRIMARY KEY AUTOINCREMENT,
          path           TEXT NOT NULL,
          building_type  TEXT NOT NULL CHECK (building_type IN ('housing','commercial')),
          kind           TEXT NOT NULL CHECK (kind IN ('rubric','candidate')),
          content_hash   TEXT,
          created_at     TEXT DEFAULT (datetime('now')),
          UNIQUE(path, kind)
        );
        CREATE TABLE IF NOT EXISTS chunks (
          id             INTEGER PRIMARY KEY AUTOINCREMENT,
          document_id    INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
          chunk_idx      INTEGER NOT NULL,
          chunk_label    TEXT,
          heading_level  INTEGER,
          path           TEXT,
          text           TEXT NOT NULL,
          clean_text     TEXT NOT NULL,
          embedding      TEXT,
          UNIQUE(document_id, chunk_idx)
        );
        CREATE TABLE IF NOT EXISTS comparisons (
          id                  INTEGER PRIMARY KEY AUTOINCREMENT,
          rubric_document_id  INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
          candidate_document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
          mode                TEXT NOT NULL,
          model               TEXT NOT NULL,
          threshold_strong    REAL NOT NULL,
          threshold_partial   REAL NOT NULL,
          strong_count        INTEGER,
          partial_count       INTEGER,
          missing_count       INTEGER,
          overall_score       REAL,
          created_at          TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS chunk_matches (
          id                 INTEGER PRIMARY KEY AUTOINCREMENT,
          comparison_id      INTEGER NOT NULL REFERENCES comparisons(id) ON DELETE CASCADE,
          rubric_chunk_id    INTEGER NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
          candidate_chunk_id INTEGER REFERENCES chunks(id) ON DELETE CASCADE,
          similarity         REAL NOT NULL,
          status             TEXT NOT NULL CHECK (status IN ('strong','partial','missing')),
          rubric_path        TEXT,
          candidate_path     TEXT,
          rubric_excerpt     TEXT,
          candidate_excerpt  TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_documents_kind ON documents(kind);
        CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks(document_id);
        CREATE INDEX IF NOT EXISTS idx_chunk_matches_comp ON chunk_matches(comparison_id);
        """
    )


def upsert_document(con: sqlite3.Connection, path: Path, building_type: str, kind: str, content_hash: str) -> Tuple[int, bool]:
    cur = con.execute("SELECT id, content_hash, building_type FROM documents WHERE path = ? AND kind = ?", (str(path), kind))
    row = cur.fetchone()
    if row:
        doc_id, existing_hash, existing_bt = row
        if existing_hash != content_hash or existing_bt != building_type:
            con.execute(
                "UPDATE documents SET building_type = ?, content_hash = ? WHERE id = ?",
                (building_type, content_hash, doc_id),
            )
            con.execute("DELETE FROM chunks WHERE document_id = ?", (doc_id,))
            return doc_id, True
        return doc_id, False

    cur = con.execute(
        "INSERT INTO documents (path, building_type, kind, content_hash) VALUES (?, ?, ?, ?)",
        (str(path), building_type, kind, content_hash),
    )
    return cur.lastrowid, True


def load_chunks(con: sqlite3.Connection, doc_id: int) -> List[Chunk]:
    cur = con.execute(
        "SELECT id, chunk_idx, chunk_label, heading_level, path, text, clean_text, embedding FROM chunks WHERE document_id = ? ORDER BY chunk_idx",
        (doc_id,),
    )
    rows = cur.fetchall()
    chunks = []
    for row in rows:
        emb = json.loads(row[7]) if row[7] else None
        chunks.append(
            Chunk(
                idx=row[1],
                label=row[2] or "chunk",
                heading_level=row[3] or 0,
                path=row[4] or "",
                text=row[5],
                clean_text=row[6],
                embedding=emb,
                db_id=row[0],
            )
        )
    return chunks


def persist_chunks(con: sqlite3.Connection, doc_id: int, chunks: List[Chunk]) -> None:
    con.execute("DELETE FROM chunks WHERE document_id = ?", (doc_id,))
    for ch in chunks:
        cur = con.execute(
            """
            INSERT INTO chunks (document_id, chunk_idx, chunk_label, heading_level, path, text, clean_text, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                doc_id,
                ch.idx,
                ch.label,
                ch.heading_level,
                ch.path,
                ch.text,
                ch.clean_text,
                json.dumps(ch.embedding) if ch.embedding is not None else None,
            ),
        )
        ch.db_id = cur.lastrowid


def coverage(rubric_chunks: List[Chunk], cand_chunks: List[Chunk]) -> List[dict]:
    results = []
    for r in rubric_chunks:
        best = None
        best_sim = -1.0
        for c in cand_chunks:
            if r.embedding is None or c.embedding is None:
                continue
            sim = cosine(r.embedding, c.embedding)
            if sim > best_sim:
                best_sim, best = sim, c
        status = "missing"
        if best_sim >= STRONG_THRESHOLD:
            status = "strong"
        elif best_sim >= PARTIAL_THRESHOLD:
            status = "partial"
        results.append(
            {
                "rubric_chunk": r,
                "candidate_chunk": best,
                "similarity": best_sim if best_sim >= 0 else 0.0,
                "status": status,
            }
        )
    return results


def overall_score(results: List[dict]) -> float:
    if not results:
        return 0.0
    total = len(results)
    strong = sum(1 for r in results if r["status"] == "strong")
    partial = sum(1 for r in results if r["status"] == "partial")
    return (strong + 0.5 * partial) / total


def persist_comparison(con: sqlite3.Connection, rubric_doc_id: int, cand_doc_id: int, model: str, results: List[dict]) -> int:
    strong = sum(1 for r in results if r["status"] == "strong")
    partial = sum(1 for r in results if r["status"] == "partial")
    missing = sum(1 for r in results if r["status"] == "missing")
    score = overall_score(results)

    cur = con.execute(
        """
        INSERT INTO comparisons (
            rubric_document_id, candidate_document_id, mode, model,
            threshold_strong, threshold_partial,
            strong_count, partial_count, missing_count, overall_score
        ) VALUES (?, ?, 'coverage', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            rubric_doc_id,
            cand_doc_id,
            model,
            STRONG_THRESHOLD,
            PARTIAL_THRESHOLD,
            strong,
            partial,
            missing,
            score,
        ),
    )
    comp_id = cur.lastrowid

    for row in results:
        r = row["rubric_chunk"]
        c = row["candidate_chunk"]
        con.execute(
            """
            INSERT INTO chunk_matches (
                comparison_id, rubric_chunk_id, candidate_chunk_id,
                similarity, status, rubric_path, candidate_path,
                rubric_excerpt, candidate_excerpt
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                comp_id,
                r.db_id,
                c.db_id if c else None,
                round(row["similarity"], 6),
                row["status"],
                r.path,
                c.path if c else None,
                r.clean_text[:200],
                c.clean_text[:200] if c else None,
            ),
        )

    return comp_id


def slugify(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_").lower()
    return text or "chunk"


# -------- WEIGHTING (explicit label→weight mappings) --------
# Keys are lowercase substrings looked for in chunk.clean_text or chunk.path.
HOUSING_LABEL_WEIGHTS = {
    # Essential interior/exterior markers
    "tactile walking surface indicator": 3.0,
    "tactile attention indicator": 3.0,
    "attention indicator": 3.0,
    "tactile direction indicator": 3.0,
    "tactile guidance": 3.0,
    "guidance bar": 2.5,
    "high contrast stair": 2.5,
    "stair nosing": 2.5,
    "braille": 2.5,
    "tactile signage": 2.5,
    "visual contrast": 2.0,
    "photoluminescent": 2.5,
    "audible beacon": 2.5,
    "audio cue": 2.0,
    # Structural markers
    "grab bar": 2.5,
    "lever handle": 2.0,
    "lowered switch": 2.0,
    "controls height": 2.0,
    "curbless": 2.5,
    "walk-in shower": 2.5,
    "wide doorway": 2.5,
    "wide hall": 2.0,
}

COMMERCIAL_LABEL_WEIGHTS = {
    # Visual contrast and cues
    "colour contrast": 2.5,
    "color contrast": 2.5,
    "doorway differentiation": 2.5,
    # Emergency/safety markers
    "photoluminescent": 3.0,
    "visual alarm": 3.0,
    "strobe": 3.0,
    # Wayfinding tools
    "tactile map": 3.0,
    "you are here": 3.0,
    "clear signage": 2.5,
    "wayfinding": 2.5,
    # Parking / entrance
    "accessible parking": 2.5,
    "access aisle": 2.5,
    # Critical areas
    "guidance bar": 2.5,
    "anti-slip nosing": 2.5,
    "warning dome": 3.0,
    "tactile attention indicator": 3.0,
    "elevator landing": 2.5,
    "washroom": 2.0,
}


def chunk_weight(building_type: str, chunk: Chunk) -> float:
    text = (chunk.clean_text + " " + chunk.path).lower()
    weight_map = HOUSING_LABEL_WEIGHTS if building_type == "housing" else COMMERCIAL_LABEL_WEIGHTS
    matched = [w for key, w in weight_map.items() if key in text]
    if matched:
        return max(matched)  # strongest applicable weight
    return 1.0  # default weight


def compute_weights(building_type: str, rubric_chunks: List[Chunk]) -> List[float]:
    raw = [chunk_weight(building_type, ch) for ch in rubric_chunks]
    total = sum(raw) or 1.0
    return [w / total for w in raw]


def ensure_project_assessment(
    con: sqlite3.Connection,
    candidate_name: str,
    building_type: str,
    score: float,
    results: List[dict],
) -> None:
    cur = con.execute("SELECT id FROM projects WHERE name = ? AND building_type = ?", (candidate_name, building_type))
    row = cur.fetchone()
    if row:
        project_id = row[0]
    else:
        cur = con.execute(
            "INSERT INTO projects (name, building_type, address) VALUES (?, ?, ?)",
            (candidate_name, building_type, None),
        )
        project_id = cur.lastrowid

    cur = con.execute(
        "INSERT INTO assessments (project_id, overall_score, rubric_version, notes) VALUES (?, ?, ?, ?)",
        (project_id, score, "v1", "Auto-generated from chunk coverage"),
    )
    assessment_id = cur.lastrowid

    # Compute rubric-specific weights (prioritised features) and normalise.
    weights = compute_weights(building_type, [r["rubric_chunk"] for r in results])

    for row, weight in zip(results, weights):
        status = row["status"]
        r_chunk: Chunk = row["rubric_chunk"]
        c_chunk: Chunk | None = row["candidate_chunk"]
        item_score = 1.0 if status == "strong" else 0.5 if status == "partial" else 0.0
        key = f"{slugify(r_chunk.label)}_{r_chunk.idx}"
        label = r_chunk.label
        evidence = c_chunk.clean_text if c_chunk else "Not found"
        con.execute(
            """
            INSERT OR REPLACE INTO assessment_items (
                assessment_id, criterion_key, criterion_label, weight,
                score, evidence, source_doc, page_numbers, category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                assessment_id,
                key,
                label,
                weight,
                item_score,
                evidence,
                candidate_name,
                None,
                None,
            ),
        )

    return None


def main():
    parser = argparse.ArgumentParser(description="Compare Markdown docs to rubric using embeddings and store results.")
    parser.add_argument("--candidate", required=True, help="Path to candidate .md file or directory of .md files")
    parser.add_argument("--rubric-housing", default=str(DEFAULT_RUBRIC_HOUSING))
    parser.add_argument("--rubric-commercial", default=str(DEFAULT_RUBRIC_COMMERCIAL))
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--env-file", default=str(DEFAULT_ENV))
    parser.add_argument("--model", default="text-embedding-3-small")
    parser.add_argument("--write-assessment", action="store_true", help="Also create a project+assessment with the coverage score")
    args = parser.parse_args()

    env = load_env(Path(args.env_file))
    api_key = env.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY missing in .env or environment.")
    client = OpenAI(api_key=api_key)

    cand_path = Path(args.candidate)
    candidates = [cand_path] if cand_path.is_file() else sorted(cand_path.glob("*.md"))
    if not candidates:
        raise SystemExit(f"No markdown files found at {cand_path}")

    rubric_paths = {
        "housing": Path(args.rubric_housing),
        "commercial": Path(args.rubric_commercial),
    }
    for key, path in rubric_paths.items():
        if not path.exists():
            raise SystemExit(f"Rubric file not found for {key}: {path}")

    con = sqlite3.connect(args.db)
    ensure_schema(con)

    for cand in candidates:
        cand_text = cand.read_text(encoding="utf-8", errors="replace")
        building_type = detect_building_type(cand_text)
        rubric_path = rubric_paths[building_type]
        rubric_text = rubric_path.read_text(encoding="utf-8", errors="replace")

        # Hashes for cache control
        cand_hash = sha256_text(cand_text)
        rubric_hash = sha256_text(rubric_text)

        rubric_chunks = chunk_markdown(rubric_text, "rubric")
        cand_chunks = chunk_markdown(cand_text, "candidate")

        rubric_doc_id, rubric_dirty = upsert_document(con, rubric_path, building_type, "rubric", rubric_hash)
        cand_doc_id, cand_dirty = upsert_document(con, cand, building_type, "candidate", cand_hash)

        cached_rubric_chunks = load_chunks(con, rubric_doc_id) if not rubric_dirty else []
        cached_cand_chunks = load_chunks(con, cand_doc_id) if not cand_dirty else []

        # Use cached embeddings if counts match and all present; otherwise re-embed.
        def needs_embed(cached: List[Chunk], fresh: List[Chunk]) -> bool:
            if len(cached) != len(fresh):
                return True
            return any(ch.embedding is None for ch in cached)

        if needs_embed(cached_rubric_chunks, rubric_chunks):
            embed_chunks(client, args.model, rubric_chunks)
            persist_chunks(con, rubric_doc_id, rubric_chunks)
        else:
            rubric_chunks = cached_rubric_chunks

        if needs_embed(cached_cand_chunks, cand_chunks):
            embed_chunks(client, args.model, cand_chunks)
            persist_chunks(con, cand_doc_id, cand_chunks)
        else:
            cand_chunks = cached_cand_chunks

        results = coverage(rubric_chunks, cand_chunks)
        comp_id = persist_comparison(con, rubric_doc_id, cand_doc_id, args.model, results)
        score = overall_score(results)
        con.commit()

        print(f"\n=== {cand.name} ({building_type}) vs {rubric_path.name} ===")
        print(f"Comparison id: {comp_id}")
        strong = sum(1 for r in results if r['status'] == 'strong')
        partial = sum(1 for r in results if r['status'] == 'partial')
        missing = sum(1 for r in results if r['status'] == 'missing')
        print(f"Strong: {strong}, Partial: {partial}, Missing: {missing}, Score: {score:.3f}")
        for row in results:
            r = row["rubric_chunk"]
            c = row["candidate_chunk"]
            print(
                f"[{row['status']:7}] sim={row['similarity']:.3f} "
                f"rubric={r.idx}({r.path}) -> cand={c.idx if c else '—'}"
            )

        if args.write_assessment:
            ensure_project_assessment(con, cand.stem, building_type, score, results)
            con.commit()
            print("Assessment written to projects/assessments tables.")

    con.close()


if __name__ == "__main__":
    main()
