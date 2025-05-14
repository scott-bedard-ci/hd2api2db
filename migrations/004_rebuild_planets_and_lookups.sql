-- Migration: Rebuild planets and lookup tables to match live API
DROP TABLE IF EXISTS planet_environmentals;
DROP TABLE IF EXISTS planet_history;
DROP TABLE IF EXISTS major_orders;
DROP TABLE IF EXISTS planets;
DROP TABLE IF EXISTS biomes;
DROP TABLE IF EXISTS environmentals;

CREATE TABLE biomes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE environmentals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE planets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    biome_id INT,
    FOREIGN KEY (biome_id) REFERENCES biomes(id)
);

CREATE TABLE planet_environmentals (
    planet_id INT NOT NULL,
    environmental_id INT NOT NULL,
    PRIMARY KEY (planet_id, environmental_id),
    FOREIGN KEY (planet_id) REFERENCES planets(id),
    FOREIGN KEY (environmental_id) REFERENCES environmentals(id)
);

CREATE TABLE planet_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    planet_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    status VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (planet_id) REFERENCES planets(id)
);

CREATE TABLE major_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    target_planet_id INT,
    expiry_time DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (target_planet_id) REFERENCES planets(id)
); 