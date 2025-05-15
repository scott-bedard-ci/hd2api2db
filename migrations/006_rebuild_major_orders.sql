-- Migration: Rebuild major_orders table to match actual API response structure
DROP TABLE IF EXISTS major_orders;

CREATE TABLE major_orders (
    id32 BIGINT PRIMARY KEY,
    expires_in INT,
    expiry_time DATETIME,
    progress JSON,
    flags INT,
    override_brief TEXT,
    override_title VARCHAR(255),
    reward JSON,
    rewards JSON,
    task_description TEXT,
    tasks JSON,
    order_type INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_expiry_time (expiry_time),
    INDEX idx_order_type (order_type)
); 