import streamlit as st

from queries import get_indicators
from calculations import calculate_indicators

from charts import (
    mortality_by_age,
    population_by_age,
    expected_cost_by_age,
    risk_distribution
)



st.set_page_config(
    page_title="Actuarial Analytics",
    layout="wide"
)



st.title(
    "📊 Actuarial Analytics"
)


st.write(
    "Indicadores atuariais gerados pelo pipeline Airflow"
)



# =====================================================
# Carregar dados Gold
# =====================================================

df = get_indicators()



# =====================================================
# Sidebar - Parâmetros
# =====================================================

st.sidebar.header(
    "Parâmetros da simulação"
)



# -------------------------
# Estado
# -------------------------

states = [
    "Todos"
] + sorted(
    df["state_code"].unique()
)


selected_state = st.sidebar.selectbox(
    "Estado",
    states
)



# -------------------------
# Sexo
# -------------------------

sex_options = [
    "Todos"
] + sorted(
    df["sex"].unique()
)


selected_sex = st.sidebar.selectbox(
    "Sexo",
    sex_options
)



# -------------------------
# Ano
# -------------------------

years = [
    "Todos"
] + sorted(
    df["reference_year"].unique(),
    reverse=True
)


selected_year = st.sidebar.selectbox(
    "Ano",
    years
)



# -------------------------
# Faixa etária
# -------------------------

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



age_options = [
    "Todos"
]


for _, row in age_ranges.iterrows():

    age_options.append(
        f"{row['age_min']}-{row['age_max']}"
    )



selected_age = st.sidebar.selectbox(
    "Faixa etária",
    age_options
)



# -------------------------
# Capital segurado
# -------------------------

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



# =====================================================
# Aplicar filtros
# =====================================================

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



# =====================================================
# Validação
# =====================================================

if filtered_df.empty:

    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )

    st.stop()



# =====================================================
# Cálculos atuariais
# =====================================================

result_df = calculate_indicators(
    filtered_df,
    insured_capital
)



# =====================================================
# Variáveis atuariais
# =====================================================

population = (
    result_df["population"]
    .sum()
)


expected_deaths = (
    result_df["expected_deaths"]
    .sum()
)


capital_exposed = (
    result_df["exposure_capital"]
    .sum()
)


expected_claim_cost = (
    result_df["expected_claim_cost"]
    .sum()
)



pure_premium = (
    expected_claim_cost
    /
    population
)



mortality = (
    result_df["mortality_rate"]
    .mean()
    *
    100
)



risk_level = (
    result_df["risk_level"].mode()[0]
    if "risk_level" in result_df.columns
    else "N/A"
)



# =====================================================
# Resumo atuarial
# =====================================================

st.subheader(
    "📌 Resumo da simulação"
)



col1, col2, col3 = st.columns(3)



with col1:

    st.metric(
        "População analisada",
        f"{population:,.0f}"
    )


    st.metric(
        "Mortes esperadas",
        f"{expected_deaths:,.2f}"
    )



with col2:

    st.metric(
        "Capital exposto",
        f"R$ {capital_exposed:,.2f}"
    )


    st.metric(
        "Custo esperado total",
        f"R$ {expected_claim_cost:,.2f}"
    )



with col3:

    st.metric(
        "Capital segurado individual",
        f"R$ {insured_capital:,.2f}"
    )


    st.metric(
        "Prêmio puro anual",
        f"R$ {pure_premium:,.2f}"
    )



st.metric(
    "Taxa média de mortalidade",
    f"{mortality:.4f}%"
)



# =====================================================
# Cenário analisado
# =====================================================

st.subheader(
    "🎯 Cenário analisado"
)



scenario_text = f"""

**Parâmetros selecionados**

- 📅 Ano: {selected_year}
- 📍 Estado: {selected_state}
- 👤 Sexo: {selected_sex}
- 🎂 Faixa etária: {selected_age}


**Exposição atuarial**

- 👥 População exposta: {population:,.0f} vidas
- 💰 Capital segurado individual: R$ {insured_capital:,.2f}
- 🏦 Capital total exposto: R$ {capital_exposed:,.2f}


**Resultado do modelo**

- ⚰️ Mortes esperadas: {expected_deaths:,.2f}
- 💸 Custo esperado total: R$ {expected_claim_cost:,.2f}
- 📌 Prêmio puro anual estimado: R$ {pure_premium:,.2f}
- 🚦 Classificação de risco: **{risk_level}**


O prêmio puro representa apenas o custo esperado do risco biométrico,
sem carregamentos administrativos, despesas comerciais,
margem de segurança ou lucro.
"""


st.info(
    scenario_text
)



# =====================================================
# Gráficos
# =====================================================

st.subheader(
    "📊 Análise gráfica atuarial"
)



tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Mortalidade",
        "População",
        "Custo esperado",
        "Risco"
    ]
)



with tab1:

    fig = mortality_by_age(
        filtered_df
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



with tab2:

    fig = population_by_age(
        filtered_df
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



with tab3:

    fig = expected_cost_by_age(
        result_df
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



with tab4:

    fig = risk_distribution(
        filtered_df
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )



# =====================================================
# Tabela final
# =====================================================

st.subheader(
    "Indicadores calculados"
)



st.dataframe(
    result_df,
    use_container_width=True
)