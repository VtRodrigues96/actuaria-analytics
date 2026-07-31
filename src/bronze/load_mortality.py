from sqlalchemy import text

from src.database.connection import get_engine
from src.extract.datasus import extract_mortality_data


def load_mortality():

    df = extract_mortality_data()

    engine = get_engine()

    insert_query = """
    INSERT INTO bronze.mortality_raw
    (
        reference_year,
        state_code,
        sex,
        age_group,
        cause_code,
        deaths,
        source,
        ingestion_timestamp
    )
    VALUES
    (
        :reference_year,
        :state_code,
        :sex,
        :age_group,
        :cause_code,
        :deaths,
        :source,
        :ingestion_timestamp
    )
    ON CONFLICT
    (
        reference_year,
        state_code,
        sex,
        age_group,
        cause_code
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

    load_mortality()

    print("Carga Bronze finalizada.")