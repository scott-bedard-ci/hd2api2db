-- Migration: Rebuild war_info, planet_infos, and home_worlds tables to match new API structure
SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS home_worlds;
DROP TABLE IF EXISTS planet_infos;
DROP TABLE IF EXISTS war_info;

SET FOREIGN_KEY_CHECKS=1;

CREATE TABLE war_info (
    war_id INT PRIMARY KEY,
    start_date DATETIME,
    end_date DATETIME,
    layout_version INT,
    minimum_client_version VARCHAR(20),
    capital_infos JSON,
    planet_permanent_effects JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE planet_infos (
    war_id INT NOT NULL,
    planet_id INT NOT NULL,
    position_x FLOAT,
    position_y FLOAT,
    waypoints JSON,
    sector INT,
    max_health BIGINT,
    disabled BOOLEAN,
    initial_faction_id INT,
    PRIMARY KEY (war_id, planet_id),
    FOREIGN KEY (war_id) REFERENCES war_info(war_id),
    FOREIGN KEY (planet_id) REFERENCES planets(id),
    FOREIGN KEY (initial_faction_id) REFERENCES factions(id)
);

CREATE TABLE home_worlds (
    war_id INT NOT NULL,
    faction_id INT NOT NULL,
    planet_id INT NOT NULL,
    PRIMARY KEY (war_id, faction_id, planet_id),
    FOREIGN KEY (war_id) REFERENCES war_info(war_id),
    FOREIGN KEY (faction_id) REFERENCES factions(id),
    FOREIGN KEY (planet_id) REFERENCES planets(id)
); 