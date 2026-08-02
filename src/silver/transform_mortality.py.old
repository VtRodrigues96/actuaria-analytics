from sqlalchemy import text

from src.database.connection import get_engine


def transform_mortality():

    engine = get_engine()

    select_query = """
    SELECT
        reference_year,
        state_code,
        sex,
        age_group,
        cause_code,
        deaths,
        source
    FROM bronze.mortality_raw;
    """

    insert_query = """
    INSERT INTO silver.mortality_clean
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max,
        cause_code,
        deaths,
        source
    )
    VALUES
    (
        :reference_year,
        :state_code,
        :sex,
        :age_min,
        :age_max,
        :cause_code,
        :deaths,
        :source
    )
    ON CONFLICT
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max,
        cause_code
    )
    DO NOTHING;
    """

    with engine.begin() as connection:

        result = connection.execute(
            text(select_query)
        )

        rows = result.fetchall()

        for row in rows:

            age_range = row.age_group.split("-")

            age_min = int(age_range[0])
            age_max = int(age_range[1])

            connection.execute(
                text(insert_query),
                {
                    "reference_year": row.reference_year,
                    "state_code": row.state_code,
                    "sex": row.sex,
                    "age_min": age_min,
                    "age_max": age_max,
                    "cause_code": row.cause_code,
                    "deaths": row.deaths,
                    "source": row.source
                }
            )


if __name__ == "__main__":

    transform_mortality()

    print("Transformação Silver mortalidade finalizada.")