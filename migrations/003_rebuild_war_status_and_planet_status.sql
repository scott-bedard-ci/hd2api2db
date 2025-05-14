-- Migration: Rebuild war_status and planet_status tables to match live API
DROP TABLE IF EXISTS planet_status;
DROP TABLE IF EXISTS war_status;

CREATE TABLE war_status (
    war_id INT PRIMARY KEY,
    time DATETIME NOT NULL,
    impact_multiplier FLOAT,
    story_beat_id32 INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE planet_status (
    war_id INT NOT NULL,
    planet_index INT NOT NULL,
    owner INT,
    health BIGINT,
    regen_per_second FLOAT,
    players INT,
    position_x FLOAT,
    position_y FLOAT,
    PRIMARY KEY (war_id, planet_index),
    FOREIGN KEY (war_id) REFERENCES war_status(war_id)
); 