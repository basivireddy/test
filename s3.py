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
