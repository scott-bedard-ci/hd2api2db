-- Wipe and Rebuild Database Schema
SET FOREIGN_KEY_CHECKS=0;

-- Drop all relevant tables if they exist
DROP TABLE IF EXISTS planet_environmentals;
DROP TABLE IF EXISTS planet_history;
DROP TABLE IF EXISTS major_orders;
DROP TABLE IF EXISTS campaigns;
DROP TABLE IF EXISTS news;
DROP TABLE IF EXISTS war_status;
DROP TABLE IF EXISTS planet_status;
DROP TABLE IF EXISTS planets;
DROP TABLE IF EXISTS biomes;
DROP TABLE IF EXISTS environmentals;
DROP TABLE IF EXISTS factions;

SET FOREIGN_KEY_CHECKS=1;

-- Run all migration scripts in order
-- (You will need to run each migration file manually after this wipe, as MySQL does not support sourcing multiple files in a single script)
-- Example:
-- SOURCE migrations/001_create_schema.sql;
-- SOURCE migrations/002_update_news_table.sql;
-- ...
-- Or run from shell: for f in migrations/00*.sql; do mysql -u $DB_USER -p$DB_PASSWORD $DB_NAME < $f; done 