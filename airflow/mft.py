from airflow import DAG
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.amazon.aws.transfers.sftp_to_s3 import SFTPToS3Operator
from datetime import datetime

# Define SFTP & S3 credentials
SFTP_CONN_ID = "aws_mft_sftp"  # Airflow connection ID
S3_BUCKET_NAME = "my-mft-bucket"  # Target S3 bucket
S3_KEY = "uploaded-files/myfile.txt"  # Target S3 path
LOCAL_FILE_PATH = "/tmp/myfile.txt"  # Local file path
REMOTE_FILE_PATH = "/upload/myfile.txt"  # Remote SFTP path

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 21),
    "retries": 1,
}

with DAG("dag_send_file_to_aws_mft",
         default_args=default_args,
         schedule=None,
         catchup=False) as dag:

    # Upload file to AWS Transfer Family (SFTP)
    upload_to_sftp = SFTPOperator(
        task_id="upload_to_sftp",
        ssh_conn_id=SFTP_CONN_ID,
        local_filepath=LOCAL_FILE_PATH,
        remote_filepath=REMOTE_FILE_PATH,
        operation="put",
        create_intermediate_dirs=True
    )



    # Define task order
    upload_to_sftp 
