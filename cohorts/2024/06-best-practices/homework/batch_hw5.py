#!/usr/bin/env python
# coding: utf-8
import os

import sys
import pickle
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
options = {
    'client_kwargs': {
        'endpoint_url': os.environ['S3_ENDPOINT_URL']
    }
}

# df = pd.read_parquet('s3://bucket/file.parquet', storage_options=options)
# df.to_parquet('s3://bucket/file.parquet', storage_options=options)

def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)

def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)

def read_data(filename, categorical):
    root_data_dir = '~/Downloads/data'
    file_name = filename.split('/')[-1]

    input_file_local = os.path.join(root_data_dir, file_name)
    if os.getenv('S3_ENDPOINT_URL') is not None and 's3://' in filename:
        print('Reading from S3: %s' % filename)
        df = pd.read_parquet(filename, storage_options=options)
    elif not os.path.exists(input_file_local):
        print('reading from local file: %s' % filename)
        df = pd.read_parquet(filename)
        df.to_parquet(input_file_local)
        print('File saved to local cash: %s' % input_file_local)
    else:
        df = pd.read_parquet(input_file_local)
    if categorical is None:
        categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df

def prepare_data(df):
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    return df

def save_data(df, output_file):
    if 's3://' in output_file:
        df.to_parquet(
            output_file,
            engine='pyarrow',
            compression=None,
            index=False,
            storage_options=options
        )
    else:
        df.to_parquet(output_file, engine='pyarrow', index=False)
    print('Data saved to %s' % output_file)

def main(year, month):
    # file_name = f'yellow_tripdata_{year:04d}-{month:02d}.parquet'
    # input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}'
    # output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']
    df = read_data(input_file, categorical)
    df = prepare_data(df)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')


    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    save_data(df_result, output_file)
    print('all done')

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.mkdir('output')
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year, month)
    # print(get_input_path(year, month))
    # print(get_output_path(year, month))