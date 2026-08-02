import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv(".env.streamlit")


def get_connection():

    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")


    url = (
        f"postgresql+psycopg2://"
        f"{user}:{password}@{host}:{port}/{database}"
    )


    engine = create_engine(url)

    return engine