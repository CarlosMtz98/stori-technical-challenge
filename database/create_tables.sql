CREATE TABLE Transaction (
    Id SERIAL PRIMARY KEY,
    Datetime TIMESTAMP NOT NULL,
    Amount NUMERIC(10, 2) NOT NULL,
    Type VARCHAR NOT NULL ,
    IdempotencyId UUID
);