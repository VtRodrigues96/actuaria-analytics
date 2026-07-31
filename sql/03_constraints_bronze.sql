ALTER TABLE bronze.mortality_raw
ADD CONSTRAINT uq_mortality_raw_business_key
UNIQUE (
    reference_year,
    state_code,
    sex,
    age_group,
    cause_code
);