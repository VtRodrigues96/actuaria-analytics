import streamlit as st

from queries import get_indicators



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



df = get_indicators()



st.metric(
    "Total de registros",
    len(df)
)



st.dataframe(
    df
)