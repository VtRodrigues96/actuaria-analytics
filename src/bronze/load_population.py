from sqlalchemy import text

from src.database.connection import get_engine
from src.extract.ibge import extract_population_data


def load_population():

    df = extract_population_data()

    engine = get_engine()

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

    with engine.begin() as connection:

        for _, row in df.iterrows():

            connection.execute(
                text(insert_query),
                row.to_dict()
            )


if __name__ == "__main__":

    load_population()

    print("Carga Bronze população finalizada.")