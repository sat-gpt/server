DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_uuid VARCHAR(64) PRIMARY KEY,
    credit_satoshis INT NOT NULL DEFAULT 0
);