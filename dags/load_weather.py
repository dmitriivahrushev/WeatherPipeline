from airflow.models.dag import DAG
import pendulum
from airflow.operators.python import PythonOperator
from core.python_scripts.utils import etl
from core.python_scripts.cities import CITIES


with DAG(
        dag_id='weather_etl',
        schedule='@daily',
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        tags=["russian_city", "weather"]
) as dag:
    etl = PythonOperator(
        task_id='weather_etl',
        python_callable=etl,
        op_kwargs={"city": CITIES}
    )
    etl
    