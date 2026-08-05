CREATE TABLE IF NOT EXISTS bronze.population_raw (

    id BIGSERIAL PRIMARY KEY,

    reference_year INTEGER NOT NULL,

    state_code VARCHAR(2) NOT NULL,

    sex VARCHAR(20),

    age_group VARCHAR(50),

    population INTEGER NOT NULL,

    source VARCHAR(50) DEFAULT 'IBGE',

    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_population_raw_business_key
        UNIQUE (
            reference_year,
            state_code,
            sex,
            age_group
        )

);