-- Migration: Add new fields to planet_history to match actual API response
ALTER TABLE planet_history
    ADD COLUMN current_health BIGINT AFTER status,
    ADD COLUMN max_health BIGINT AFTER current_health,
    ADD COLUMN player_count INT AFTER max_health;
-- Optionally, allow timestamp to be NULL for flexibility (uncomment if needed):
-- ALTER TABLE planet_history MODIFY COLUMN timestamp DATETIME NULL; 