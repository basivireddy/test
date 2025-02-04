from airflow import DAG
import pendulum
import requests
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Set the local timezone
local_timezone = pendulum.timezone("Australia/Sydney")

# Define the function to invoke the AWS Lambda via ALB
def invoke_lambda_via_alb(**kwargs):
    alb_url = "https://your-alb-endpoint.com/path-to-lambda"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "key1": "value1",
        "key2": "value2"
    }
    
    response = requests.post(alb_url, json=payload, headers=headers, verify=False)  # disable ssl
    
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)

# Define the DAG
with DAG(
    dag_id='lambda_invoke_dag',
    default_args=default_args,
    description='A simple DAG to invoke an AWS Lambda function via ALB',
    schedule_interval=None,  # Manual trigger
    start_date=datetime(2024, 1, 1, tzinfo=local_timezone),
    catchup=False,
    access_control={
        'commsurv_rd': {'can_dag_read'},
        'commsurv_op': {'can_dag_edit', 'can_dag_read'}
    }
) as dag:

    invoke_lambda_task = PythonOperator(
        task_id='invoke_lambda',
        python_callable=invoke_lambda_via_alb,
        provide_context=True
    )

invoke_lambda_task
