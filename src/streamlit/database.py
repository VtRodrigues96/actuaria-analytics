import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Carrega configuração exclusiva do Streamlit
load_dotenv(".env.streamlit")


def get_streamlit_engine():

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")


    url = (
        f"postgresql+psycopg2://"
        f"{user}:{password}@{host}:{port}/{database}"
    )


    return create_engine(url)