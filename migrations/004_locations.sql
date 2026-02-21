-- 004_locations.sql
CREATE TABLE IF NOT EXISTS locations (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  name         TEXT,
  address      TEXT,
  latitude     REAL NOT NULL,
  longitude    REAL NOT NULL,
  source_doc   TEXT,
  created_at   TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_locations_coords ON locations(latitude, longitude);
