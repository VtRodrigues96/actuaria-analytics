from sqlalchemy import text

from src.database.connection import get_engine


def calculate_risk_level(mortality_rate):

    mortality_rate = float(mortality_rate)

    if mortality_rate < 0.001:
        return "LOW"

    elif mortality_rate < 0.01:
        return "MEDIUM"

    else:
        return "HIGH"



def transform_mortality():

    engine = get_engine()


    select_query = """
    SELECT
        age,
        sex,
        mortality_rate,
        life_expectancy,
        source
    FROM bronze.mortality_table_raw;
    """


    insert_query = """
    INSERT INTO silver.mortality_clean
    (
        age,
        sex,
        mortality_rate,
        survival_probability,
        life_expectancy,
        risk_level,
        source
    )
    VALUES
    (
        :age,
        :sex,
        :mortality_rate,
        :survival_probability,
        :life_expectancy,
        :risk_level,
        :source
    )

    ON CONFLICT
    (
        age,
        sex
    )

    DO UPDATE SET

        mortality_rate = EXCLUDED.mortality_rate,

        survival_probability = EXCLUDED.survival_probability,

        life_expectancy = EXCLUDED.life_expectancy,

        risk_level = EXCLUDED.risk_level,

        source = EXCLUDED.source;
    """



    inserted = 0


    with engine.begin() as connection:


        rows = connection.execute(
            text(select_query)
        ).fetchall()



        for row in rows:


            mortality_rate = float(
                row.mortality_rate
            )


            survival_probability = (
                1 - mortality_rate
            )


            risk_level = calculate_risk_level(
                mortality_rate
            )



            connection.execute(
                text(insert_query),
                {
                    "age": row.age,

                    "sex": row.sex,

                    "mortality_rate": mortality_rate,

                    "survival_probability": survival_probability,

                    "life_expectancy": row.life_expectancy,

                    "risk_level": risk_level,

                    "source": row.source
                }
            )


            inserted += 1



    print(
        f"Silver mortalidade finalizada: {inserted} registros"
    )



if __name__ == "__main__":

    transform_mortality()