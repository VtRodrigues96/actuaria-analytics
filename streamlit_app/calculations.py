import pandas as pd


def calculate_indicators(df, insured_capital):

    df = df.copy()


    df["insured_capital"] = insured_capital


    df["expected_claim_cost"] = (
        df["expected_deaths"]
        *
        insured_capital
    )


    df["pure_premium"] = (
        df["expected_claim_cost"]
        /
        df["population"]
    )


    return df