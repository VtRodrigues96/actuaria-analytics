from sqlalchemy import text

from src.database.connection import get_engine
from src.extract.ibge_mortality import extract_mortality_table


def load_mortality_table():

    engine = get_engine()

    df = extract_mortality_table()

    insert_query = """
    INSERT INTO bronze.mortality_table_raw
    (
        age,
        sex,
        mortality_rate,
        life_expectancy,
        source,
        ingestion_timestamp
    )
    VALUES
    (
        :age,
        :sex,
        :mortality_rate,
        :life_expectancy,
        :source,
        :ingestion_timestamp
    )

    ON CONFLICT
    (
        age,
        sex
    )

    DO UPDATE SET

        mortality_rate = EXCLUDED.mortality_rate,

        life_expectancy = EXCLUDED.life_expectancy,

        source = EXCLUDED.source,

        ingestion_timestamp = EXCLUDED.ingestion_timestamp;

    """

    processed = 0


    with engine.begin() as connection:

        for _, row in df.iterrows():

            result = connection.execute(
                text(insert_query),
                {
                    "age": int(row["age"]),

                    "sex": str(row["sex"]),

                    "mortality_rate": float(
                        row["mortality_rate"]
                    ),

                    "life_expectancy": (
                        float(row["life_expectancy"])
                        if row["life_expectancy"] is not None
                        else None
                    ),

                    "source": row.get(
                        "source",
                        "IBGE"
                    ),

                    "ingestion_timestamp": (
                        row["ingestion_timestamp"]
                    )
                }
            )


            processed += result.rowcount



    print(
        f"Carga Bronze mortalidade IBGE finalizada: {processed} registros processados"
    )


    return processed



if __name__ == "__main__":

    load_mortality_table()