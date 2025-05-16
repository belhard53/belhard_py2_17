CREATE TABLE IF NOT EXISTS test_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO test_table (name) VALUES ('Test Data 3'), ('Test Data 4');