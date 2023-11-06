CREATE TABLE IF NOT EXISTS transaction (
    id SERIAL PRIMARY KEY,
    datetime TIMESTAMP NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    type VARCHAR NOT NULL ,
    idempotency_id UUID
);

CREATE TABLE IF NOT EXISTS recipient (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);