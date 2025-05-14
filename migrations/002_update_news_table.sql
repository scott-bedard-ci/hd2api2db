-- Migration: Rebuild news table to match live API fields
DROP TABLE IF EXISTS news;

CREATE TABLE news (
    id INT PRIMARY KEY,
    published DATETIME NOT NULL,
    type VARCHAR(100) NOT NULL,
    tagIds JSON NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 