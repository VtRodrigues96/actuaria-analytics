import plotly.express as px



def mortality_by_age(df):

    mortality = (
        df.groupby(
            [
                "age_min",
                "age_max"
            ],
            as_index=False
        )
        [
            "mortality_rate"
        ]
        .mean()
    )


    mortality["age_group"] = (
        mortality["age_min"].astype(str)
        +
        "-"
        +
        mortality["age_max"].astype(str)
    )


    fig = px.line(
        mortality,
        x="age_group",
        y="mortality_rate",
        markers=True,
        title="Taxa de Mortalidade por Faixa Etária"
    )


    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Taxa de Mortalidade"
    )


    return fig





def population_by_age(df):

    population = (
        df.groupby(
            [
                "age_min",
                "age_max"
            ],
            as_index=False
        )
        [
            "population"
        ]
        .sum()
    )


    population["age_group"] = (
        population["age_min"].astype(str)
        +
        "-"
        +
        population["age_max"].astype(str)
    )


    fig = px.bar(
        population,
        x="age_group",
        y="population",
        title="População por Faixa Etária"
    )


    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Quantidade de vidas"
    )


    return fig





def expected_cost_by_age(df):

    cost = (
        df.groupby(
            [
                "age_min",
                "age_max"
            ],
            as_index=False
        )
        [
            "expected_claim_cost"
        ]
        .sum()
    )


    cost["age_group"] = (
        cost["age_min"].astype(str)
        +
        "-"
        +
        cost["age_max"].astype(str)
    )


    fig = px.bar(
        cost,
        x="age_group",
        y="expected_claim_cost",
        title="Custo Esperado por Faixa Etária"
    )


    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Custo esperado (R$)"
    )


    return fig





def risk_distribution(df):

    risk = (
        df["risk_level"]
        .value_counts()
        .reset_index()
    )


    risk.columns = [
        "risk_level",
        "quantity"
    ]


    fig = px.pie(
        risk,
        names="risk_level",
        values="quantity",
        title="Distribuição de Risco"
    )


    return fig