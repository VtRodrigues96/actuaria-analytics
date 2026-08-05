from sqlalchemy import text

from src.database.connection import get_engine
from src.extract.ibge import extract_population_data


def load_population():

    engine = get_engine()

    df = extract_population_data()


    insert_query = """
    INSERT INTO bronze.population_raw
    (
        reference_year,
        state_code,
        sex,
        age_group,
        population,
        source,
        ingestion_timestamp
    )
    VALUES
    (
        :reference_year,
        :state_code,
        :sex,
        :age_group,
        :population,
        :source,
        :ingestion_timestamp
    )

    ON CONFLICT
    (
        reference_year,
        state_code,
        sex,
        age_group
    )

    DO NOTHING;
    """


    inserted = 0


    with engine.begin() as connection:

        for _, row in df.iterrows():

            result = connection.execute(
                text(insert_query),
                {
                    "reference_year": int(
                        row["reference_year"]
                    ),

                    "state_code": row["state_code"],

                    "sex": row["sex"],

                    "age_group": row["age_group"],

                    "population": int(
                        row["population"]
                    ),

                    "source": row["source"],

                    "ingestion_timestamp": row[
                        "ingestion_timestamp"
                    ]
                }
            )


            inserted += result.rowcount


    print(
        f"Carga Bronze população IBGE finalizada: {inserted} registros novos inseridos"
    )


    return inserted



if __name__ == "__main__":

    load_population()