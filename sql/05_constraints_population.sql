ALTER TABLE bronze.population_raw
ADD CONSTRAINT uq_population_raw_business_key
UNIQUE (
    reference_year,
    state_code,
    sex,
    age_group
);