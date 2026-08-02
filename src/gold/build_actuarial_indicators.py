import pandas as pd

from sqlalchemy import text

from src.database.connection import get_engine



def execute_query(query):

    engine = get_engine()

    with engine.connect() as conn:

        result = conn.execute(
            text(query)
        )

        df = pd.DataFrame(
            result.fetchall(),
            columns=result.keys()
        )

    return df




def load_population():

    query = """
    SELECT *
    FROM silver.population_clean;
    """

    return execute_query(query)




def load_mortality():

    query = """
    SELECT *
    FROM silver.mortality_age_group;
    """

    return execute_query(query)




def merge_tables():

    population = load_population().copy()

    mortality = load_mortality().copy()


    population["age_max"] = (
        population["age_max"]
        .fillna(999)
        .astype(int)
    )


    mortality["age_max"] = (
        mortality["age_max"]
        .fillna(999)
        .astype(int)
    )



    df = population.merge(

        mortality,

        on=[

            "sex",
            "age_min",
            "age_max"

        ],

        how="left"

    )


    print(
        f"Registros após merge: {len(df)}"
    )



    missing = (
        df["avg_mortality_rate"]
        .isna()
        .sum()
    )


    print(
        f"Mortabilidades não encontradas: {missing}"
    )



    df = df.dropna(

        subset=[

            "avg_mortality_rate",
            "avg_life_expectancy"

        ]

    )


    return df





def calculate_actuarial_indicators(df):


    df = df.copy()



    df.loc[:, "expected_deaths"] = (

        df["population"]

        *

        df["avg_mortality_rate"]

    )



    df.loc[:, "expected_survivors"] = (

        df["population"]

        -

        df["expected_deaths"]

    )




    def classify_risk(rate):

        if rate < 0.005:

            return "BAIXO"


        elif rate < 0.03:

            return "MODERADO"


        else:

            return "ALTO"




    df.loc[:, "risk_level"] = (

        df["avg_mortality_rate"]

        .apply(classify_risk)

    )


    return df






def save_gold(df):


    engine = get_engine()



    insert_query = """

    INSERT INTO gold.actuarial_indicators

    (

        reference_year,

        state_code,

        sex,

        age_min,

        age_max,

        population,

        mortality_rate,

        life_expectancy,

        expected_deaths,

        expected_survivors,

        risk_level,

        source

    )


    VALUES

    (

        :reference_year,

        :state_code,

        :sex,

        :age_min,

        :age_max,

        :population,

        :mortality_rate,

        :life_expectancy,

        :expected_deaths,

        :expected_survivors,

        :risk_level,

        :source

    )



    ON CONFLICT

    (

        reference_year,

        state_code,

        sex,

        age_min,

        age_max

    )


    DO UPDATE SET


        population =
            EXCLUDED.population,


        mortality_rate =
            EXCLUDED.mortality_rate,


        life_expectancy =
            EXCLUDED.life_expectancy,


        expected_deaths =
            EXCLUDED.expected_deaths,


        expected_survivors =
            EXCLUDED.expected_survivors,


        risk_level =
            EXCLUDED.risk_level,


        source =
            EXCLUDED.source,


        processing_timestamp =
            CURRENT_TIMESTAMP;

    """



    records = []



    for _, row in df.iterrows():


        records.append(

            {

                "reference_year":
                    row.reference_year,


                "state_code":
                    row.state_code,


                "sex":
                    row.sex,


                "age_min":
                    row.age_min,


                # CORREÇÃO PRINCIPAL
                # Mantém 999 para 90+

                "age_max":
                    int(row.age_max),



                "population":
                    row.population,


                "mortality_rate":
                    row.avg_mortality_rate,


                "life_expectancy":
                    row.avg_life_expectancy,


                "expected_deaths":
                    row.expected_deaths,


                "expected_survivors":
                    row.expected_survivors,


                "risk_level":
                    row.risk_level,


                "source":
                    "IBGE"

            }

        )




    with engine.begin() as conn:

        conn.execute(

            text(insert_query),

            records

        )



    print(
        f"Indicadores Gold carregados: {len(records)}"
    )






def validate_dataframe(df):


    print()

    print("==============================")

    print("VALIDAÇÃO GOLD ACTUARIAL")

    print("==============================")


    print(
        f"Quantidade de registros: {len(df)}"
    )



    print()

    print("Estados:")

    print(

        df["state_code"]
        .unique()

    )



    print()

    print("Sexos:")

    print(

        df["sex"]
        .unique()

    )



    print()

    print("Riscos:")

    print(

        df["risk_level"]
        .value_counts()

    )



    duplicates = (

        df.groupby(

            [

                "reference_year",
                "state_code",
                "sex",
                "age_min",
                "age_max"

            ]

        )

        .size()

        .reset_index(name="count")

    )


    duplicates = duplicates[

        duplicates["count"] > 1

    ]



    print()

    print("Duplicidades antes da carga:")


    print(

        len(duplicates)

    )







def build_actuarial_indicators():


    df = merge_tables()


    df = calculate_actuarial_indicators(df)


    validate_dataframe(df)


    save_gold(df)


    return df






if __name__ == "__main__":


    print()

    print("==============================")

    print("GOLD ACTUARIAL PIPELINE")

    print("==============================")


    build_actuarial_indicators()