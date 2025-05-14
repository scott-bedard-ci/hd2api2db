-- Migration: Rebuild campaigns and factions tables to match live API
DROP TABLE IF EXISTS campaigns;
DROP TABLE IF EXISTS factions;

CREATE TABLE factions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    planet_index INT NOT NULL,
    biome_id INT,
    faction_id INT,
    defense BOOLEAN,
    expire_datetime DATETIME,
    health INT,
    max_health INT,
    percentage FLOAT,
    players INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (biome_id) REFERENCES biomes(id),
    FOREIGN KEY (faction_id) REFERENCES factions(id)
); 