-- 003_chunk_vectors.sql
-- Stores chunk-level embeddings and comparison results between rubric docs and candidate docs.

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
  mode                TEXT NOT NULL, -- coverage|diff|alignment
  model               TEXT NOT NULL,
  threshold_strong    REAL NOT NULL,
  threshold_partial   REAL NOT NULL,
  strong_count        INTEGER,
  partial_count       INTEGER,
  missing_count       INTEGER,
  overall_score       REAL, -- normalized coverage score
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
