import pandas as pd
from datetime import datetime

from src.config.settings import config


STATE = config["data"]["state"]
START_YEAR = config["data"]["start_year"]
END_YEAR = config["data"]["end_year"]


def extract_mortality_data():
    """
    Extrai dados históricos de mortalidade.

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
                "cause_code": "I10",

                # Simulação de evolução histórica
                # posteriormente será substituído pelo DATASUS real
                "deaths": 1200 + ((year - START_YEAR) * 15)
            }
        )


    df = pd.DataFrame(data)

    df["source"] = config["mortality"]["source"]

    df["ingestion_timestamp"] = datetime.now()

    return df



if __name__ == "__main__":

    mortality_df = extract_mortality_data()

    print(mortality_df)