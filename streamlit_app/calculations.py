import pandas as pd


def calculate_indicators(df, insured_capital):

    df = df.copy()


    # Capital segurado individual
    df["insured_capital"] = insured_capital


    # Capital total exposto
    df["exposure_capital"] = (
        df["population"]
        *
        insured_capital
    )


    # Custo esperado de sinistros
    df["expected_claim_cost"] = (
        df["expected_deaths"]
        *
        insured_capital
    )


    # Prêmio puro individual
    df["pure_premium"] = (
        df["expected_claim_cost"]
        /
        df["population"]
    )


    return df