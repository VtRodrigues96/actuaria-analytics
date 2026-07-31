CREATE TABLE IF NOT EXISTS bronze.mortality_raw (

    id BIGSERIAL PRIMARY KEY,

    reference_year INTEGER NOT NULL,

    state_code VARCHAR(2) NOT NULL,

    sex VARCHAR(20),

    age_group VARCHAR(50),

    cause_code VARCHAR(10),

    deaths INTEGER NOT NULL,

    source VARCHAR(50) DEFAULT 'DATASUS',

    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);