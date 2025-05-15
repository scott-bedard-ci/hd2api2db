-- Migration: Create Helldivers 2 Data Schema
-- Run this script to set up the initial database schema

CREATE TABLE IF NOT EXISTS planets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(255),
    liberation_status VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS war_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    active_players INT,
    -- Add other relevant fields as needed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    publish_date DATETIME,
    -- Add other relevant fields as needed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    start_date DATETIME,
    end_date DATETIME,
    -- Add other relevant fields as needed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS major_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT,
    target_planet_id INT,
    expiry_time DATETIME,
    -- Add other relevant fields as needed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (target_planet_id) REFERENCES planets(id)
);

CREATE TABLE IF NOT EXISTS planet_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    planet_id INT NOT NULL,
    timestamp DATETIME NOT NULL,
    status VARCHAR(100),
    -- Add other relevant fields as needed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (planet_id) REFERENCES planets(id)
);

-- Indexes for efficient querying
CREATE INDEX idx_planet_history_planet_id ON planet_history(planet_id);
CREATE INDEX idx_major_orders_target_planet_id ON major_orders(target_planet_id); 