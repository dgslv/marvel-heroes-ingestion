CREATE SCHEMA datalake;

CREATE TABLE IF NOT EXISTS datalake.raw_marvel_heroes (
    id SERIAL PRIMARY KEY,
    ingestion_timestamp INT,
    payload text NOT NULL
);