-- Active: 1684257232396@@lallah.db.elephantsql.com@5432
-- Drop the table if it exists (for rollback/reversal)
DROP TABLE IF EXISTS invoices;

-- Create the table
CREATE TABLE invoices (
    r_hash VARCHAR(64) PRIMARY KEY,
    query TEXT,
    used BOOLEAN NOT NULL DEFAULT FALSE,
    chat_history JSONB NOT NULL DEFAULT '[]'
);

--Create User ID TABLE 
CREATE TABLE user_ids (
    uuid PRIMARY KEY,
    chats JSONB NOT NULL DEFAULT '[]', 
    chat_history JSONB NOT NULL DEFAULT '[]'
)
