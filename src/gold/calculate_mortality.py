from sqlalchemy import text

from src.database.connection import get_engine


def calculate_mortality():

    engine = get_engine()

    select_query = """
    SELECT
        m.reference_year,
        m.state_code,
        m.sex,
        m.age_min,
        m.age_max,
        m.deaths,
        p.population
    FROM silver.mortality_clean m

    INNER JOIN silver.population_clean p

    ON
        m.reference_year = p.reference_year
        AND m.state_code = p.state_code
        AND m.sex = p.sex
        AND m.age_min = p.age_min
        AND m.age_max = p.age_max;
    """


    insert_query = """
    INSERT INTO gold.mortality_indicators
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max,
        deaths,
        population,
        mortality_rate
    )
    VALUES
    (
        :reference_year,
        :state_code,
        :sex,
        :age_min,
        :age_max,
        :deaths,
        :population,
        :mortality_rate
    )

    ON CONFLICT
    (
        reference_year,
        state_code,
        sex,
        age_min,
        age_max
    )

    DO UPDATE SET

        deaths = EXCLUDED.deaths,

        population = EXCLUDED.population,

        mortality_rate = EXCLUDED.mortality_rate;
    """


    with engine.begin() as connection:

        result = connection.execute(
            text(select_query)
        )

        rows = result.fetchall()


        for row in rows:

            mortality_rate = (
                row.deaths / row.population
            ) * 100000


            connection.execute(
                text(insert_query),
                {
                    "reference_year": row.reference_year,
                    "state_code": row.state_code,
                    "sex": row.sex,
                    "age_min": row.age_min,
                    "age_max": row.age_max,
                    "deaths": row.deaths,
                    "population": row.population,
                    "mortality_rate": round(
                        mortality_rate,
                        2
                    )
                }
            )


if __name__ == "__main__":

    calculate_mortality()

    print("Cálculo Gold de mortalidade finalizado.")