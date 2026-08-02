CREATE TABLE IF NOT EXISTS silver.mortality_age_group (

    id BIGSERIAL PRIMARY KEY,

    age_min INTEGER NOT NULL,

    age_max INTEGER,

    sex VARCHAR(1) NOT NULL,

    avg_mortality_rate NUMERIC(12,10) NOT NULL,

    avg_life_expectancy NUMERIC(10,4),

    source VARCHAR(50) DEFAULT 'IBGE',

    processing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_mortality_age_group
    UNIQUE
    (
        age_min,
        age_max,
        sex
    )
);