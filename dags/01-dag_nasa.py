from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow import DAG


with DAG(dag_id="01-dag_nasa",
    description="Nasa generando OK en txt",
    schedule_interval = '@hourly',
    start_date=datetime(2023, 2, 13, 0, 0, 0),
    end_date=datetime(2023, 2, 13, 5, 0, 0),
    max_active_runs = 1) as dag:
    t1= BashOperator(
        task_id="Permission_generation",
        bash_command='sleep 20 && echo "OK" > /tmp/responses/response_{{ds_nodash}}_{{ execution_date.strftime("%H%M%S") }}.txt'
    )
    t1