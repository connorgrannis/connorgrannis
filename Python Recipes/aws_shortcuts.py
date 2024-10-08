import boto3
import pandas as pd
import io

def download_csv_from_s3(bucket_name, file_key, local_save_path, return_df=False):
    # Initialize a session using Boto3
    s3 = boto3.client('s3')
    # Download the CSV file from S3 as a stream
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    # Read the content of the file
    content = response['Body'].read().decode('utf-8')
    # Use StringIO to convert the content into a file-like object
    csv_data = io.StringIO(content)
    # Load CSV data into a pandas DataFrame
    df = pd.read_csv(csv_data)
    df.to_csv(local_save_path)
    print(f"CSV file downloaded and saved to {local_save_path}")
    if return_df:
        return df

