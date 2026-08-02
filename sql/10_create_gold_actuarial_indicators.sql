CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.actuarial_indicators (

    id BIGSERIAL PRIMARY KEY,

    reference_year INTEGER NOT NULL,

    state_code VARCHAR(2) NOT NULL,

    sex VARCHAR(1) NOT NULL,

    age_min INTEGER NOT NULL,

    age_max INTEGER,

    population INTEGER NOT NULL,

    mortality_rate NUMERIC(12,10) NOT NULL,

    life_expectancy NUMERIC(10,4),

    expected_deaths NUMERIC(14,2),

    expected_survivors NUMERIC(14,2),

    insured_capital NUMERIC(14,2),

    expected_claim_cost NUMERIC(16,2),

    pure_premium NUMERIC(14,4),

    risk_level VARCHAR(20),

    source VARCHAR(50) DEFAULT 'IBGE',

    processing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_gold_actuarial
    UNIQUE (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max
    )
);