CREATE TABLE IF NOT EXISTS bronze.mortality_table_raw (

    id BIGSERIAL PRIMARY KEY,

    age INTEGER NOT NULL,

    sex VARCHAR(1) NOT NULL,

    mortality_rate NUMERIC(12,10) NOT NULL,

    life_expectancy NUMERIC(10,4),

    source VARCHAR(50) DEFAULT 'IBGE',

    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_mortality_table_business_key
        UNIQUE (
            age,
            sex
        )

);