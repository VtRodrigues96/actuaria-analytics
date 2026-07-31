import pandas as pd
from datetime import datetime

from src.config.settings import config


STATE = config["data"]["state"]
START_YEAR = config["data"]["start_year"]
END_YEAR = config["data"]["end_year"]


def extract_population_data():
    """
    Extrai dados históricos populacionais.

    Retorna:
        pandas.DataFrame
    """

    data = []

    for year in range(START_YEAR, END_YEAR + 1):

        data.append(
            {
                "reference_year": year,
                "state_code": STATE,
                "sex": "M",
                "age_group": "60-69",

                # Simulação histórica para validação do pipeline.
                # Posteriormente será substituído pela fonte oficial IBGE.
                "population": 850000 + ((year - START_YEAR) * 5000)
            }
        )


    df = pd.DataFrame(data)

    df["source"] = config["population"]["source"]

    df["ingestion_timestamp"] = datetime.now()

    return df



if __name__ == "__main__":

    population_df = extract_population_data()

    print(population_df)