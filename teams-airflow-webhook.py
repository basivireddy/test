from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

# Microsoft Teams Webhook URL (Replace with your actual webhook URL)
TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/YOUR_WEBHOOK_URL"

# Function to send message
def send_teams_message():
    message = {
        "text": "✅ Airflow DAG executed successfully!"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(TEAMS_WEBHOOK_URL, headers=headers, data=json.dumps(message))

    if response.status_code != 200:
        raise ValueError(f"Request to Teams returned {response.status_code}, {response.text}")

# Define Airflow DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='send_teams_message',
    default_args=default_args,
    schedule_interval='@daily',  # Adjust as needed
    catchup=False
) as dag:

    notify_teams = PythonOperator(
        task_id='notify_teams',
        python_callable=send_teams_message
    )

    notify_teams
