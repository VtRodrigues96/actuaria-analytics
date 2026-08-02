import pandas as pd
from datetime import datetime

from src.config.settings import config


START_YEAR = config["data"]["historical"]["start_year"]
END_YEAR = config["data"]["historical"]["end_year"]

STATES = config["data"]["states"]

FILE_PATH = "/opt/airflow/data/ibge/populacao_ibge.xlsx"

SHEET_NAME = "2) POP_GRUPO QUINQUENAL"


def extract_population_data():

    """
    Extrai população do arquivo oficial IBGE.

    Fonte:
    Projeções das Populações - Revisão 2024

    Dados utilizados:
    - Estado
    - Sexo
    - Grupo etário quinquenal
    - Ano

    Retorna:
        pandas.DataFrame
    """


    # =====================================
    # LEITURA DO EXCEL
    # =====================================

    df = pd.read_excel(
        FILE_PATH,
        sheet_name=SHEET_NAME,
        header=5
    )


    # =====================================
    # RENOMEAR COLUNAS
    # =====================================

    df = df.rename(
        columns={
            "GRUPO ETÁRIO": "age_group",
            "SEXO": "sex",
            "SIGLA": "state_code"
        }
    )


    # =====================================
    # FILTRO DE ESTADOS
    # =====================================

    df = df[
        df["state_code"].isin(STATES)
    ]


    # =====================================
    # REMOVER TOTAL
    # UTILIZAR SOMENTE SEXO M/F
    # =====================================

    df = df[
        df["sex"].isin(
            [
                "Homens",
                "Mulheres"
            ]
        )
    ]


    # =====================================
    # PADRONIZAÇÃO SEXO
    # =====================================

    df["sex"] = df["sex"].replace(
        {
            "Homens": "M",
            "Mulheres": "F"
        }
    )


    # =====================================
    # LIMPEZA FAIXA ETÁRIA
    # =====================================

    df["age_group"] = (
        df["age_group"]
        .astype(str)
        .str.strip()
    )


    # =====================================
    # SELEÇÃO DOS ANOS DISPONÍVEIS
    # =====================================

    year_columns = [
        year
        for year in range(
            START_YEAR,
            END_YEAR + 1
        )
        if year in df.columns
    ]


    if not year_columns:

        raise Exception(
            "Nenhuma coluna de ano encontrada no arquivo IBGE"
        )


    # =====================================
    # TRANSFORMAÇÃO WIDE -> LONG
    # =====================================

    df = df.melt(
        id_vars=[
            "age_group",
            "sex",
            "state_code"
        ],
        value_vars=year_columns,
        var_name="reference_year",
        value_name="population"
    )


    # =====================================
    # TRATAMENTO DOS TIPOS
    # =====================================

    df["reference_year"] = (
        df["reference_year"]
        .astype(int)
    )


    df["population"] = (
        df["population"]
        .fillna(0)
        .astype(int)
    )


    # =====================================
    # METADADOS
    # =====================================

    df["source"] = "IBGE"

    df["ingestion_timestamp"] = datetime.now()


    # =====================================
    # ORDEM FINAL DA BRONZE
    # =====================================

    df = df[
        [
            "reference_year",
            "state_code",
            "sex",
            "age_group",
            "population",
            "source",
            "ingestion_timestamp"
        ]
    ]


    return df



if __name__ == "__main__":


    population_df = extract_population_data()


    print(population_df.head(20))


    print("\nQuantidade de registros:")
    print(population_df.shape)


    print("\nEstados:")
    print(
        population_df["state_code"]
        .unique()
    )


    print("\nSexos:")
    print(
        population_df["sex"]
        .unique()
    )


    print("\nFaixas etárias:")
    print(
        population_df["age_group"]
        .unique()
    )