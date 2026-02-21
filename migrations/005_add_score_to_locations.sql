-- 005_add_score_to_locations.sql
ALTER TABLE locations ADD COLUMN score REAL;
ALTER TABLE locations ADD COLUMN comparison_id INTEGER;
CREATE INDEX IF NOT EXISTS idx_locations_score ON locations(score);
