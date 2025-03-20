import boto3
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def list_s3_files():
    s3 = boto3.client("s3")
    bucket_name = "your-bucket-name"
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix="your-prefix/")

    files = [obj["Key"] for obj in response.get("Contents", [])]
    print("Files in S3:", files)
    return files

with DAG(
    "list_s3_files_boto3",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    list_files_task = PythonOperator(
        task_id="list_files_task",
        python_callable=list_s3_files,
    )
