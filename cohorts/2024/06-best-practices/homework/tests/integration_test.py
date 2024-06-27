import os
import pandas as pd
from datetime import datetime

from batch_hw5 import get_input_path, get_output_path, options, save_data

from datetime import datetime
import boto3

import pytest

# Configure the Boto3 client to use LocalStack
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

def list_objects_with_sizes(bucket_name, file_name):
    print('Searching for %s...' % file_name)
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            if file_name in obj['Key']:
                file_size = obj['Size']
                print(f"Object: {obj['Key']} - Size: {file_size:.2f} bytes")
    else:
        print(f"No objects found in {bucket_name}")

def list_buckets():
    response = s3.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    return buckets

def s3_search_file(file_path):
    file_name = file_path.split('/')[-1]
    buckets = list_buckets()
    for bucket in buckets:
        list_objects_with_sizes(bucket, file_name)

def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)

data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df_input = pd.DataFrame(data, columns=columns)

TEST_YEAR = 2023
TEST_MONTH = 1
input_file = get_input_path(year=TEST_YEAR, month=TEST_MONTH)
save_data(df_input, input_file)
s3_search_file(input_file)

os.system(f'python batch_hw5.py {TEST_YEAR} {TEST_MONTH}')

output_file = get_output_path(TEST_YEAR, TEST_MONTH)
result_df = pd.read_parquet(output_file, storage_options=options)

assert result_df['predicted_duration'].sum() == pytest.approx(36.28, abs=1e-2)
