# Define constants
S3_BUCKET_NAME = "your-s3-bucket-name"
S3_PREFIX = "your/path/in/s3/"  # Folder or specific file path
LOCAL_DOWNLOAD_PATH = "/tmp/s3_files/"
SFTP_REMOTE_PATH = "/remote/vendor/path/"
SFTP_CONN_ID = "sftp_vendor_conn"
S3_CONN_ID = "aws_s3_conn"


def download_files_from_s3():
    s3_hook = S3Hook(aws_conn_id=S3_CONN_ID)
    files = s3_hook.list_keys(bucket_name=S3_BUCKET_NAME, prefix=S3_PREFIX)
    
    if not files:
        raise ValueError("No files found in S3 with the specified prefix.")

    os.makedirs(LOCAL_DOWNLOAD_PATH, exist_ok=True)

    for file_key in files:
        local_file_path = os.path.join(LOCAL_DOWNLOAD_PATH, os.path.basename(file_key))
        s3_hook.download_file(bucket_name=S3_BUCKET_NAME, key=file_key, local_path=local_file_path)
        print(f"Downloaded: {file_key} → {local_file_path}")



from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define constants
S3_BUCKET_NAME = "your-bucket-name"
S3_FILE_KEY = "uploads/my_uploaded_file.txt"  # Destination path in S3
LOCAL_FILE_PATH = "/tmp/sample_file.txt"
AWS_CONN_ID = "aws_default"  # Update if using a different connection

def upload_file_to_s3():
    """Upload a file from local storage to an S3 bucket."""
    s3_hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    
    # Upload file to S3
    s3_hook.load_file(
        filename=LOCAL_FILE_PATH,
        key=S3_FILE_KEY,
        bucket_name=S3_BUCKET_NAME,
        replace=True  # Set to False to prevent overwriting
    )
    
    print(f"File uploaded successfully to s3://{S3_BUCKET_NAME}/{S3_FILE_KEY}")

# Define the DAG
with DAG(
    dag_id="s3_upload_dag",
    start_date=datetime(2024, 3, 17),
    schedule_interval=None,  # Run manually
    catchup=False
) as dag:
    
    upload_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_file_to_s3
    )

    upload_task
