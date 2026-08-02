from sqlalchemy import text

from src.streamlit.database import get_streamlit_engine


engine = get_streamlit_engine()


with engine.connect() as conn:

    result = conn.execute(
        text(
            "SELECT 1"
        )
    )

    print(result.fetchone())