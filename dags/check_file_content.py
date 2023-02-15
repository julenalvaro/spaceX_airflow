def check_file_content(**context):
    filepath = '/tmp/responses/response_' + context['ds_nodash'] + '_' + context['execution_date'].strftime('%H%M%S') + '.txt'
    ti = context['ti']

    with open(filepath, 'r') as f:
        content = f.read()
        if content.strip() == 'OK':
            ti.xcom_push(key='permission', value=True)
        else:
            ti.xcom_push(key='permission', value=False)