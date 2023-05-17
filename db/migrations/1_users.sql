DROP TABLE IF EXISTS invoices;
CREATE TABLE users (
    user_uuid VARCHAR(64) PRIMARY KEY
    credit_satoshis INT NOT NULL DEFAULT 0
);