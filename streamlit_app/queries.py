from database import get_connection
import pandas as pd


def get_indicators():

    engine = get_connection()


    query = """

    SELECT
        reference_year,
        state_code,
        sex,
        age_min,
        age_max,
        population,
        mortality_rate,
        expected_deaths

    FROM gold.actuarial_indicators

    ORDER BY reference_year

    """


    return pd.read_sql(
        query,
        engine
    )