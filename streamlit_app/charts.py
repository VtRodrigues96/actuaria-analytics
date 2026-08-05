import plotly.express as px


def apply_layout(fig):

    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(
            l=40,
            r=40,
            t=60,
            b=40
        ),
        title_x=0.02,
        font=dict(
            size=13
        ),
        legend_title_text=""
    )

    return fig



def br_number(value):

    return (
        f"{value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )



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


    mortality["mortality_percent"] = (
        mortality["mortality_rate"]
        *
        100
    )


    fig = px.line(
        mortality,
        x="age_group",
        y="mortality_percent",
        markers=True,
        text=[
            f"{x:.2f}%"
            for x in mortality["mortality_percent"]
        ],
        title="Taxa de Mortalidade por Faixa Etária"
    )


    fig.update_traces(
        textposition="top center"
    )


    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Mortalidade (%)"
    )


    return apply_layout(fig)





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
        text_auto=True,
        title="Distribuição Populacional por Faixa Etária"
    )


    fig.update_traces(
        texttemplate="%{text}"
    )


    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Quantidade de vidas"
    )


    return apply_layout(fig)





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
        text_auto=True,
        title="Custo Esperado de Sinistros por Faixa Etária"
    )


    fig.update_layout(
        xaxis_title="Faixa Etária",
        yaxis_title="Custo esperado (R$)"
    )


    return apply_layout(fig)





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
        hole=0.35,
        title="Distribuição dos Níveis de Risco"
    )


    fig.update_traces(
        textinfo="percent+label"
    )


    return apply_layout(fig)