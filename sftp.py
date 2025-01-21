import paramiko
import os

def lambda_handler(event, context):
    # SFTP server details
    sftp_host = os.environ.get('SFTP_HOST')  # e.g., 'example.com'
    sftp_port = int(os.environ.get('SFTP_PORT', 22))  # Default port 22
    sftp_username = os.environ.get('SFTP_USERNAME')
    sftp_password = os.environ.get('SFTP_PASSWORD')  # Alternatively, use an SSH key for secure authentication
    
    try:
        # Initialize SSH client
        transport = paramiko.Transport((sftp_host, sftp_port))
        transport.connect(username=sftp_username, password=sftp_password)
        
        # Initialize SFTP client
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("SFTP connection established successfully!")
        
        # Perform a simple test operation (e.g., list files in the root directory)
        files = sftp.listdir('.')
        print(f"Files in the root directory: {files}")
        
        # Close the connection
        sftp.close()
        transport.close()
        return {
            'statusCode': 200,
            'body': 'SFTP connection test successful. Files listed successfully.'
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f"SFTP connection test failed: {str(e)}"
        }
