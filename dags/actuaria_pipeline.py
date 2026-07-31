from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

from datetime import datetime
import pendulum

from src.bronze.load_mortality import load_mortality
from src.bronze.load_population import load_population

from src.silver.transform_mortality import transform_mortality
from src.silver.transform_population import transform_population

from src.gold.calculate_mortality import calculate_mortality


local_tz = pendulum.timezone("America/Sao_Paulo")


@dag(
    dag_id="actuaria_pipeline",
    description="Pipeline atuarial utilizando arquitetura Medallion",
    schedule="0 6 * * *",
    start_date=datetime(
        2026,
        1,
        1,
        tzinfo=local_tz
    ),
    catchup=False,
    tags=[
        "actuaria",
        "medallion",
        "datasus",
        "ibge"
    ]
)
def actuaria_pipeline():


    @task
    def bronze_mortality_task():

        load_mortality()


    @task
    def bronze_population_task():

        load_population()


    @task
    def silver_mortality_task():

        transform_mortality()


    @task
    def silver_population_task():

        transform_population()


    @task
    def gold_task():

        calculate_mortality()



    with TaskGroup("bronze") as bronze:

        mortality = bronze_mortality_task()

        population = bronze_population_task()



    with TaskGroup("silver") as silver:

        mortality_clean = silver_mortality_task()

        population_clean = silver_population_task()



    with TaskGroup("gold") as gold:

        indicators = gold_task()



    bronze >> silver >> gold



actuaria_pipeline()