def retrieve_platzi_data(**kwargs):
    import pandas as pd
    data = pd.DataFrame({"student": ["Maria Cruz", "Daniel Crema",
    "Elon Musk", "Karol Castrejon", "Freddy Vega"],
    "timestamp": [kwargs['logical_date'],
    kwargs['logical_date'], kwargs['logical_date'], kwargs['logical_date'],
    kwargs['logical_date']]})

    #Consultamos si hay permiso para descargar datos
    permission = bool(kwargs["ti"].xcom_pull(task_ids='read_file',key='permission'))

    if permission:
        data.to_csv(f"/tmp/platzi_data/platzi_data_{kwargs['ds_nodash']}_{kwargs['execution_date'].strftime('%H%M%S')}.csv",
        header=True)
    
    else:
        raise ValueError("No hay permiso para descargar datos")