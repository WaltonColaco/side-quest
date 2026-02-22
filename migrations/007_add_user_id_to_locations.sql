-- Migration 007: link each location to the Django auth_user who uploaded it.
-- user_id is nullable so existing rows (and anonymous uploads) are not broken.
ALTER TABLE locations ADD COLUMN user_id INTEGER;
