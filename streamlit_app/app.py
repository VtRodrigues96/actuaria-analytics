import streamlit as st

from queries import get_indicators
from calculations import calculate_indicators


st.set_page_config(
    page_title="Actuarial Analytics",
    layout="wide"
)


st.title("📊 Actuarial Analytics")


st.write(
    "Indicadores atuariais gerados pelo pipeline Airflow"
)


# ==========================
# Carregar dados Gold
# ==========================

df = get_indicators()



# ==========================
# Sidebar - Parâmetros
# ==========================

st.sidebar.header(
    "Parâmetros da simulação"
)



# Estado

states = ["Todos"] + sorted(
    df["state_code"].unique()
)


selected_state = st.sidebar.selectbox(
    "Estado",
    states
)



# Sexo

sex_options = ["Todos"] + sorted(
    df["sex"].unique()
)


selected_sex = st.sidebar.selectbox(
    "Sexo",
    sex_options
)



# Ano

years = ["Todos"] + sorted(
    df["reference_year"].unique(),
    reverse=True
)


selected_year = st.sidebar.selectbox(
    "Ano",
    years
)



# Faixa etária

age_ranges = (
    df[
        [
            "age_min",
            "age_max"
        ]
    ]
    .drop_duplicates()
    .sort_values(
        [
            "age_min",
            "age_max"
        ]
    )
)


age_options = ["Todos"]


for _, row in age_ranges.iterrows():

    age_options.append(
        f"{row['age_min']}-{row['age_max']}"
    )


selected_age = st.sidebar.selectbox(
    "Faixa etária",
    age_options
)



# Capital segurado

capital_options = [
    50000,
    100000,
    250000,
    500000,
    1000000
]


insured_capital = st.sidebar.selectbox(
    "Capital segurado (R$)",
    capital_options,
    format_func=lambda x: f"R$ {x:,.2f}"
)



# ==========================
# Aplicar filtros
# ==========================

filtered_df = df.copy()



if selected_state != "Todos":

    filtered_df = filtered_df[
        filtered_df["state_code"]
        ==
        selected_state
    ]



if selected_sex != "Todos":

    filtered_df = filtered_df[
        filtered_df["sex"]
        ==
        selected_sex
    ]



if selected_year != "Todos":

    filtered_df = filtered_df[
        filtered_df["reference_year"]
        ==
        selected_year
    ]



if selected_age != "Todos":

    age_min, age_max = selected_age.split("-")


    filtered_df = filtered_df[
        (filtered_df["age_min"] == int(age_min))
        &
        (filtered_df["age_max"] == int(age_max))
    ]



# ==========================
# Cálculos atuariais
# ==========================

result_df = calculate_indicators(
    filtered_df,
    insured_capital
)



# ==========================
# Resumo atuarial
# ==========================

st.subheader(
    "📌 Resumo da simulação"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "População analisada",
        f"{result_df['population'].sum():,.0f}"
    )


    st.metric(
        "Mortes esperadas",
        f"{result_df['expected_deaths'].sum():,.2f}"
    )



with col2:

    st.metric(
        "Capital segurado",
        f"R$ {insured_capital:,.2f}"
    )


    st.metric(
        "Custo esperado total",
        f"R$ {result_df['expected_claim_cost'].sum():,.2f}"
    )



with col3:

    avg_premium = (
        result_df["pure_premium"]
        .mean()
    )


    mortality = (
        result_df["mortality_rate"]
        .mean()
        *
        100
    )


    st.metric(
        "Prêmio puro médio anual",
        f"R$ {avg_premium:,.2f}"
    )


    st.metric(
        "Taxa média de mortalidade",
        f"{mortality:.4f}%"
    )



# ==========================
# Explicação atuarial
# ==========================

st.info(
    """
    **Interpretação atuarial**

    Os valores apresentados representam estimativas de risco biométrico.

    - O custo esperado considera pagamento integral do capital segurado
      em caso de ocorrência do evento de morte.
    - O prêmio puro representa o custo médio esperado por indivíduo.
    - Não estão considerados carregamentos administrativos, margem de segurança,
      despesas comerciais ou lucro.
    """
)



# ==========================
# Tabela final
# ==========================

st.subheader(
    "Indicadores calculados"
)


st.dataframe(
    result_df,
    use_container_width=True
)