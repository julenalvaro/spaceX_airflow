from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from check_file_content import check_file_content
from generate_platzi_data import retrieve_platzi_data
from email_generator import send_email_marketing, send_email_data_team

with DAG(dag_id="02-DAG_principal",
    description="DAG principal",
    schedule_interval="@hourly",
    start_date=datetime(2023, 2, 13, 0, 0, 0),
    end_date=datetime(2023, 2, 13, 5, 0, 0),
    max_active_runs=1) as dag:
    
    # Definimos una tarea de tipo `FileSensor` que espera la llegada de un archivo en una ruta especifica
    t1 = FileSensor(task_id="waiting_file", 
                    filepath="/tmp/responses/response_{{ ds_nodash }}_{{ execution_date.strftime('%H%M%S') }}.txt")

    # Definimos una tarea de tipo `PythonOperator` que ejecuta una función `check_file_content`.
    # La opción `provide_context=True` le dice a la tarea que incluya información del contexto de ejecución.
    t2 = PythonOperator(task_id="read_file",
                        python_callable=check_file_content,
                        provide_context=True)
    
    # Definimos una tarea de tipo `PythonOperator` que ejecuta una función `retrieve_platzi_data` solo si hay permiso.
    t3 = PythonOperator(task_id="retrieve_platzi_data", 
                        python_callable=retrieve_platzi_data,
                        provide_context=True
    )

    # Definimos una tarea de tipo `BashOperator` que descarga datos de SpaceX y los guarda en un archivo en una ruta específica.
    # La opción `trigger_rule='one_success'` establece que esta tarea se ejecutará solo si al menos una tarea anterior se ha completado correctamente.
    t4= BashOperator(task_id="retrieve_spaceX_data",                  
                  bash_command="curl -o /tmp/spaceX_data/history_{{ds_nodash}}_{{ execution_date.strftime('%H%M%S') }}.json -L 'https://api.spacexdata.com/v4/history' && echo 'datos de SpaceX descargados'")
    
    # Si todo ha ido OK, enviamos un correo a los equipos responsables.
    
    t5= PythonOperator(task_id="send_email_spaceX",
                       python_callable=send_email_marketing)

    t6= PythonOperator(task_id="send_email_platzi",
                       python_callable=send_email_data_team)
    
    # La tarea 5 depende de la tarea 4, la tarea 6 depende de la tarea 3
    
t1 >> t2 >> [t3, t4]
t4 >> t5
t3 >> t6