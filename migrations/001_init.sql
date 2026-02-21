-- 001_init.sql: Rubric assessment schema
CREATE TABLE IF NOT EXISTS projects (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  name          TEXT NOT NULL,
  building_type TEXT NOT NULL CHECK (building_type IN ('housing','commercial')),
  address       TEXT,
  created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS assessments (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id     INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  overall_score  REAL NOT NULL,
  rubric_version TEXT NOT NULL DEFAULT 'v1',
  notes          TEXT,
  created_at     TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS assessment_items (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  assessment_id   INTEGER NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
  criterion_key   TEXT NOT NULL,
  criterion_label TEXT NOT NULL,
  weight          REAL NOT NULL CHECK (weight >= 0 AND weight <= 1),
  score           REAL NOT NULL CHECK (score >= 0 AND score <= 1),
  weighted_score  REAL GENERATED ALWAYS AS (weight * score) VIRTUAL,
  evidence        TEXT,
  source_doc      TEXT,
  page_numbers    TEXT,
  UNIQUE(assessment_id, criterion_key)
);

CREATE TABLE IF NOT EXISTS assessment_conflicts (
  id                   INTEGER PRIMARY KEY AUTOINCREMENT,
  assessment_item_id   INTEGER NOT NULL REFERENCES assessment_items(id) ON DELETE CASCADE,
  field_name           TEXT NOT NULL,
  value_a              TEXT,
  value_b              TEXT,
  note                 TEXT
);
