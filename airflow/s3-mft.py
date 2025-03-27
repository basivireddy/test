from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import paramiko
import os

# --- Configuration Variables ---
S3_BUCKET = 'your-bucket-name'
S3_PREFIX = 'your-folder/'  # Folder prefix in S3 (optional)
FILE_PATTERN = 'your-pattern'  # Change this to filter specific files
LOCAL_DOWNLOAD_PATH = '/tmp/s3_downloaded_file.txt'  # Local file path
SFTP_HOST = 'your-sftp-server.com'
SFTP_USERNAME = 'your-username'
SFTP_KEY_FILE = '/path/to/your/private/key.pem'
SFTP_REMOTE_PATH = '/remote/path/s3_uploaded_file.txt'  # Remote SFTP path

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    's3_to_sftp_transfer',
    default_args=default_args,
    description='List files from S3, filter, download, and transfer via SFTP',
    schedule_interval=None,  # Run manually or set a cron schedule
    catchup=False,
)

# --- Step 1: List and filter S3 files ---
def list_s3_files():
    s3_hook = S3Hook(aws_conn_id='aws_default')
    files = s3_hook.list_keys(bucket_name=S3_BUCKET, prefix=S3_PREFIX)
    
    if not files:
        raise ValueError("No files found in S3 bucket.")
    
    matched_files = [file for file in files if FILE_PATTERN in file]

    if not matched_files:
        raise ValueError("No matching files found.")

    return matched_files[0]  # Return first matched file

# --- Step 2: Download S3 file ---
def download_s3_file(**kwargs):
    ti = kwargs['ti']
    s3_hook = S3Hook(aws_conn_id='aws_default')
    
    matched_file = ti.xcom_pull(task_ids='list_s3_files')
    s3_hook.download_file(bucket_name=S3_BUCKET, key=matched_file, local_path=LOCAL_DOWNLOAD_PATH)

# --- Step 3: Transfer file via SFTP ---
def transfer_file_via_sftp():
    if not os.path.exists(LOCAL_DOWNLOAD_PATH):
        raise FileNotFoundError("Local file not found for SFTP transfer.")

    key = paramiko.RSAKey(filename=SFTP_KEY_FILE)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(hostname=SFTP_HOST, username=SFTP_USERNAME, pkey=key)
    sftp = ssh.open_sftp()
    
    sftp.put(LOCAL_DOWNLOAD_PATH, SFTP_REMOTE_PATH)
    sftp.close()
    ssh.close()

# --- Airflow Tasks ---
list_s3_task = PythonOperator(
    task_id='list_s3_files',
    python_callable=list_s3_files,
    provide_context=True,
    dag=dag,
)

download_s3_task = PythonOperator(
    task_id='download_s3_file',
    python_callable=download_s3_file,
    provide_context=True,
    dag=dag,
)

transfer_sftp_task = PythonOperator(
    task_id='transfer_file_via_sftp',
    python_callable=transfer_file_via_sftp,
    dag=dag,
)

# --- Task Dependencies ---
list_s3_task >> download_s3_task >> transfer_sftp_task
