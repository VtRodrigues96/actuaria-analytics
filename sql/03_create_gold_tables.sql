CREATE TABLE IF NOT EXISTS gold.mortality_indicators (

    id BIGSERIAL PRIMARY KEY,

    reference_year INTEGER NOT NULL,

    state_code VARCHAR(2) NOT NULL,

    sex VARCHAR(20),

    age_min INTEGER,

    age_max INTEGER,

    deaths INTEGER NOT NULL,

    population INTEGER NOT NULL,

    mortality_rate NUMERIC(10,2) NOT NULL,

    source VARCHAR(50) DEFAULT 'DATASUS_IBGE',

    calculation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT uq_mortality_indicator_business_key
    UNIQUE
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max
    )
);