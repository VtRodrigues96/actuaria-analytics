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

st.title("📊 Actuarial Analytics")
st.write("Indicadores atuariais gerados pelo pipeline Airflow")

# =====================================================
# Funções de formatação
# =====================================================

def numero(valor, casas=0):
    return (
        f"{valor:,.{casas}f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

def moeda(valor):
    return "R$ " + numero(valor, 2)

# =====================================================
# Carregar dados
# =====================================================

df = get_indicators()

# =====================================================
# Sidebar
# =====================================================

st.sidebar.header("Parâmetros da simulação")

states = ["Todos"] + sorted(df["state_code"].unique())
selected_state = st.sidebar.selectbox("Estado", states)

sex_options = ["Todos"] + sorted(df["sex"].unique())
selected_sex = st.sidebar.selectbox("Sexo", sex_options)

years = ["Todos"] + sorted(
    df["reference_year"].unique(),
    reverse=True
)
selected_year = st.sidebar.selectbox("Ano", years)

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
    format_func=moeda
)

# =====================================================
# Aplicar filtros
# =====================================================

filtered_df = df.copy()

if selected_state != "Todos":
    filtered_df = filtered_df[
        filtered_df["state_code"] == selected_state
    ]

if selected_sex != "Todos":
    filtered_df = filtered_df[
        filtered_df["sex"] == selected_sex
    ]

if selected_year != "Todos":
    filtered_df = filtered_df[
        filtered_df["reference_year"] == selected_year
    ]

if selected_age != "Todos":
    age_min, age_max = selected_age.split("-")

    filtered_df = filtered_df[
        (filtered_df["age_min"] == int(age_min))
        &
        (filtered_df["age_max"] == int(age_max))
    ]

if filtered_df.empty:
    st.warning(
        "Nenhum registro encontrado para os filtros selecionados."
    )
    st.stop()

# =====================================================
# Cálculos
# =====================================================

result_df = calculate_indicators(
    filtered_df,
    insured_capital
)

population = result_df["population"].sum()
expected_deaths = result_df["expected_deaths"].sum()
capital_exposed = result_df["exposure_capital"].sum()
expected_claim_cost = result_df["expected_claim_cost"].sum()

pure_premium = (
    expected_claim_cost
    /
    population
)

mortality = (
    result_df["mortality_rate"].mean()
    *
    100
)

risk_level = (
    result_df["risk_level"].mode()[0]
    if "risk_level" in result_df.columns
    else "N/A"
)

life_expectancy = (
    result_df["life_expectancy"].mean()
    if "life_expectancy" in result_df.columns
    else None
)

# =====================================================
# KPIs
# =====================================================

st.subheader("📌 Resumo da Simulação")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "População",
        numero(population)
    )
    st.metric(
        "Mortes Esperadas",
        numero(expected_deaths, 2)
    )

with k2:
    st.metric(
        "Capital Individual",
        moeda(insured_capital)
    )
    st.metric(
        "Capital Exposto",
        moeda(capital_exposed)
    )

with k3:
    st.metric(
        "Custo Esperado",
        moeda(expected_claim_cost)
    )
    st.metric(
        "Prêmio Puro",
        moeda(pure_premium)
    )

with k4:
    st.metric(
        "Mortalidade Média",
        numero(mortality, 4) + "%"
    )
    if life_expectancy is not None:
        st.metric(
            "Expectativa de Vida",
            numero(life_expectancy, 1) + " anos"
        )

st.subheader("🎯 Cenário Analisado")

st.success(
f"""
### Perfil Selecionado

**📅 Ano:** {selected_year}

**📍 Estado:** {selected_state}

**👤 Sexo:** {selected_sex}

**🎂 Faixa Etária:** {selected_age}

---

### Exposição Atuarial

**👥 População analisada:** {numero(population)} vidas

**💰 Capital segurado individual:** {moeda(insured_capital)}

**🏦 Capital total exposto:** {moeda(capital_exposed)}

---

### Resultado da Simulação

**⚰️ Mortes esperadas:** {numero(expected_deaths,2)}

**💸 Custo esperado total:** {moeda(expected_claim_cost)}

**📌 Prêmio puro anual:** {moeda(pure_premium)}

**🚦 Classificação de risco:** {risk_level}
"""
)

st.info(
"""
**Interpretação Atuarial**

O prêmio puro representa exclusivamente o custo esperado do risco biométrico.

Não estão considerados:

- despesas administrativas;
- carregamentos comerciais;
- margem de segurança;
- lucro;
- tributos.
"""
)

st.subheader("📈 Painel Analítico")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📉 Mortalidade",
        "👥 População",
        "💰 Custo",
        "🚦 Risco"
    ]
)

with tab1:
    st.plotly_chart(
        mortality_by_age(filtered_df),
        use_container_width=True
    )

with tab2:
    st.plotly_chart(
        population_by_age(filtered_df),
        use_container_width=True
    )

with tab3:
    st.plotly_chart(
        expected_cost_by_age(result_df),
        use_container_width=True
    )

with tab4:
    st.plotly_chart(
        risk_distribution(filtered_df),
        use_container_width=True
    )

# =====================================================
# Base detalhada
# =====================================================

st.subheader("📋 Indicadores Calculados")

display_df = result_df.copy()

display_df["population"] = display_df["population"].map(
    lambda x: numero(x)
)

display_df["expected_deaths"] = display_df["expected_deaths"].map(
    lambda x: numero(x, 2)
)

display_df["mortality_rate"] = display_df["mortality_rate"].map(
    lambda x: numero(x * 100, 4) + "%"
)

if "life_expectancy" in display_df.columns:
    display_df["life_expectancy"] = display_df["life_expectancy"].map(
        lambda x: numero(x, 1)
    )

if "insured_capital" in display_df.columns:
    display_df["insured_capital"] = display_df["insured_capital"].map(
        moeda
    )

display_df["exposure_capital"] = display_df["exposure_capital"].map(
    moeda
)

display_df["expected_claim_cost"] = display_df["expected_claim_cost"].map(
    moeda
)

if "pure_premium" in display_df.columns:
    display_df["pure_premium"] = display_df["pure_premium"].map(
        moeda
    )

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)