CREATE TABLE IF NOT EXISTS silver.mortality_clean (

    id BIGSERIAL PRIMARY KEY,

    age INTEGER NOT NULL,

    sex VARCHAR(1) NOT NULL,

    mortality_rate NUMERIC(12,10) NOT NULL,

    survival_probability NUMERIC(12,10) NOT NULL,

    life_expectancy NUMERIC(10,4),

    risk_level VARCHAR(20),

    source VARCHAR(50) DEFAULT 'IBGE',

    processing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_mortality_clean_business_key
    UNIQUE
    (
        age,
        sex
    )

);