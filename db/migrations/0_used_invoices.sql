-- Drop the table if it exists (for rollback/reversal)
DROP TABLE IF EXISTS invoices;

-- Create the table
CREATE TABLE invoices (
    r_hash VARCHAR(64) PRIMARY KEY,
    query TEXT,
    used BOOLEAN NOT NULL DEFAULT FALSE
);
