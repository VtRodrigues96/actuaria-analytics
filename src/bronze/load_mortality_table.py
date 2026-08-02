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
    DO NOTHING;
    """


    with engine.begin() as connection:

        for _, row in df.iterrows():

            connection.execute(
                text(insert_query),
                {
                    "age": int(row["age"]),
                    "sex": row["sex"],
                    "mortality_rate": row["mortality_rate"],
                    "life_expectancy": row["life_expectancy"],
                    "source": row["source"],
                    "ingestion_timestamp": row["ingestion_timestamp"]
                }
            )


    print(
        f"Carga Bronze mortalidade IBGE finalizada: {len(df)} registros"
    )


if __name__ == "__main__":

    load_mortality_table()