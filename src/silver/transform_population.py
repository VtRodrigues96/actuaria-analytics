from sqlalchemy import text

from src.database.connection import get_engine


def transform_population():

    engine = get_engine()

    select_query = """
    SELECT
        reference_year,
        state_code,
        sex,
        age_group,
        population,
        source
    FROM bronze.population_raw;
    """

    insert_query = """
    INSERT INTO silver.population_clean
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max,
        population,
        source
    )
    VALUES
    (
        :reference_year,
        :state_code,
        :sex,
        :age_min,
        :age_max,
        :population,
        :source
    )
    ON CONFLICT
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max
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
                    "population": row.population,
                    "source": row.source
                }
            )


if __name__ == "__main__":

    transform_population()

    print("Transformação Silver população finalizada.")