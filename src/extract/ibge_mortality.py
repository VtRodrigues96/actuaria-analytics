import pandas as pd
from datetime import datetime

from src.config.settings import config


BASE_PATH = "data/ibge/mortality_tables"


def load_mortality_table(file_name, sex):

    file_path = f"{BASE_PATH}/{file_name}"

    df = pd.read_excel(
        file_path,
        skiprows=5,
        header=None
    )


    df.columns = [
        "age",
        "mortality_per_mil",
        "deaths_per_mil",
        "lx",
        "lx_half",
        "tx",
        "life_expectancy"
    ]


    # Remove linhas vazias
    df = df[
        df["age"].notna()
    ]


    # Remove linha de cabeçalho residual do Excel
    df = df[
        df["age"] != "(X)"
    ]


    # Conversão segura da idade
    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )


    # Remove idades inválidas
    df = df.dropna(
        subset=["age"]
    )


    df["age"] = df["age"].astype(int)


    # Conversão dos indicadores numéricos
    df["mortality_per_mil"] = pd.to_numeric(
        df["mortality_per_mil"],
        errors="coerce"
    )


    df["life_expectancy"] = pd.to_numeric(
        df["life_expectancy"],
        errors="coerce"
    )


    # Remove registros sem taxa de mortalidade
    df = df.dropna(
        subset=["mortality_per_mil"]
    )


    # Q(X,N) está em mortes por mil habitantes
    # Converter para probabilidade
    df["mortality_rate"] = (
        df["mortality_per_mil"] / 1000
    )


    df["sex"] = sex

    df["source"] = config["population"]["source"]

    df["ingestion_timestamp"] = datetime.now()


    return df[
        [
            "age",
            "sex",
            "mortality_rate",
            "life_expectancy",
            "source",
            "ingestion_timestamp"
        ]
    ]



def extract_mortality_table():

    homens = load_mortality_table(
        "homens.xlsx",
        "M"
    )


    mulheres = load_mortality_table(
        "mulheres.xlsx",
        "F"
    )


    df = pd.concat(
        [
            homens,
            mulheres
        ],
        ignore_index=True
    )


    return df



if __name__ == "__main__":

    mortality_df = extract_mortality_table()


    print(mortality_df.head(10))


    print("\nQuantidade de registros:")
    print(mortality_df.shape)


    print("\nSexos:")
    print(
        mortality_df["sex"].unique()
    )


    print("\nIdade mínima e máxima:")
    print(
        mortality_df["age"].min(),
        mortality_df["age"].max()
    )


    print("\nRegistros inválidos:")
    print(
        mortality_df.isnull().sum()
    )