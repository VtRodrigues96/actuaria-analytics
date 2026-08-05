from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

from datetime import datetime, timedelta
from pathlib import Path

import pendulum



local_tz = pendulum.timezone(
    "America/Sao_Paulo"
)



default_args = {

    "owner": "airflow",

    "retries": 3,

    "retry_delay": timedelta(
        minutes=5
    )

}



def task_failure_callback(context):

    print("=" * 60)
    print("ERRO NA PIPELINE")
    print(f"DAG: {context['dag'].dag_id}")
    print(f"TASK: {context['task'].task_id}")
    print(f"EXECUÇÃO: {context['execution_date']}")
    print("=" * 60)





@dag(

    dag_id="actuaria_pipeline",

    description="""

    Pipeline atuarial utilizando arquitetura Medallion.

    Bronze:
        Dados brutos IBGE

    Silver:
        Dados tratados e derivados

    Gold:
        Indicadores atuariais

    """,

    schedule="0 6 * * *",

    start_date=datetime(
        2026,
        1,
        1,
        tzinfo=local_tz
    ),

    catchup=False,

    default_args=default_args,

    on_failure_callback=task_failure_callback,

    tags=[
        "atuaria",
        "medallion",
        "ibge",
        "postgres"
    ]

)


def actuaria_pipeline():



    # =====================================================
    # DATABASE INITIALIZATION
    # =====================================================


    @task(
        task_id="init_database"
    )
    def init_database():

        from sqlalchemy import text
        from src.database.connection import get_engine


        engine = get_engine()


        sql_path = Path(
            "/opt/airflow/sql"
        )


        scripts = [

            "01_create_schemas.sql",

            "04_create_population_bronze.sql",

            "06_create_mortality_table_bronze.sql",

            "02_create_silver_tables.sql",

            "07_create_silver_mortality.sql",

            "09_create_silver_mortality_age_group.sql",

            "03_create_gold_tables.sql",

            "10_create_gold_actuarial_indicators.sql"

        ]



        with engine.begin() as conn:


            for script in scripts:


                print(
                    f"Executando SQL: {script}"
                )


                sql = (
                    sql_path / script
                ).read_text()


                conn.execute(
                    text(sql)
                )


        print(
            "Banco inicializado"
        )



    database_ready = init_database()




    # =====================================================
    # BRONZE
    # =====================================================


    with TaskGroup(

        group_id="bronze",

        tooltip="Camada Bronze"

    ) as bronze:



        @task(
            task_id="load_population"
        )
        def load_population():


            from src.bronze.load_population import (
                load_population
            )


            result = load_population()


            print(
                "Bronze população concluído"
            )


            return result





        @task(
            task_id="load_mortality_table"
        )
        def load_mortality_table():


            from src.bronze.load_mortality_table import (
                load_mortality_table
            )


            result = load_mortality_table()


            print(
                "Bronze mortalidade IBGE concluído"
            )


            return result




        population = load_population()


        mortality = load_mortality_table()





    # =====================================================
    # SILVER
    # =====================================================


    with TaskGroup(

        group_id="silver",

        tooltip="Camada Silver"

    ) as silver:



        @task(
            task_id="transform_population"
        )
        def transform_population():


            from src.silver.transform_population import (
                transform_population
            )


            result = transform_population()


            print(
                "Silver população concluído"
            )


            return result





        @task(
            task_id="transform_mortality"
        )
        def transform_mortality():


            from src.silver.transform_mortality import (
                transform_mortality
            )


            result = transform_mortality()


            print(
                "Silver mortalidade base concluído"
            )


            return result





        @task(
            task_id="build_mortality_age_group"
        )
        def build_mortality_age_group():


            from src.silver.build_mortality_age_group import (
                build_mortality_age_group
            )


            result = build_mortality_age_group()


            print(
                "Silver mortalidade faixa etária concluído"
            )


            return result





        population_clean = transform_population()


        mortality_clean = transform_mortality()


        mortality_age_group = build_mortality_age_group()



        mortality_clean >> mortality_age_group





    # =====================================================
    # GOLD
    # =====================================================


    with TaskGroup(

        group_id="gold",

        tooltip="Camada Gold"

    ) as gold:



        @task(
            task_id="build_indicators"
        )
        def build_indicators():


            from src.gold.build_actuarial_indicators import (

                merge_tables,

                calculate_actuarial_indicators,

                save_gold

            )



            print(
                "Gerando indicadores atuariais"
            )



            df = merge_tables()



            df = calculate_actuarial_indicators(
                df
            )



            save_gold(
                df
            )



            print(
                f"Indicadores gerados: {len(df)}"
            )



            return len(df)





        indicators = build_indicators()






    # =====================================================
    # QUALITY CHECK
    # =====================================================


    @task(
        task_id="quality_check"
    )
    def quality_check():


        from sqlalchemy import text

        from src.database.connection import get_engine



        engine = get_engine()



        query = """

        SELECT COUNT(*)

        FROM gold.actuarial_indicators

        """



        with engine.begin() as conn:


            count = conn.execute(
                text(query)
            ).scalar()



        if count == 0:


            raise Exception(
                "Gold sem registros"
            )



        print(
            "Quality Check aprovado"
        )


        print(
            f"Registros Gold: {count}"
        )


        return count





    # =====================================================
    # DEPENDENCIES
    # =====================================================


    database_ready >> bronze


    bronze >> silver


    silver >> gold


    indicators >> quality_check()




actuaria_pipeline()