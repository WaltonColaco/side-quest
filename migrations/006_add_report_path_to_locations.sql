-- 006_add_report_path_to_locations.sql
-- Stores the absolute path to the extracted markdown report for each location.
ALTER TABLE locations ADD COLUMN report_path TEXT;
