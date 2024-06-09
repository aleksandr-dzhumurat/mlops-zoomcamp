#!/usr/bin/env python
# coding: utf-8

# In[1]:


# get_ipython().system('pip freeze | grep scikit-learn')

# get_ipython().system('python -V')


import os
import sys

import pickle
import pandas as pd
import numpy as np

with open('model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)
categorical = ['PULocationID', 'DOLocationID']


def get_file_size_in_mb(file_path):
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    return file_size_mb

def read_data(filename):
    df = pd.read_parquet(filename)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


if __name__ == '__main__':
    year = sys.argv[1]
    month = sys.argv[2]
    root_data_dir = sys.argv[3]

    # year = '2023'
    # month = '03'
    # data_dir = '~/Downloads/data'
    file_path = os.path.join(root_data_dir, f'yellow_tripdata_{year}-{month}.parquet')
    print(f'Loading data from {file_path}...')
    df = read_data(file_path)
    print('Num rows: %d. Transformation started...' % df.shape[0])
    # df = read_data(f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month}.parquet')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    std_dev = np.std(y_pred)
    mean = np.mean(y_pred)
    print("Standard Deviation: %.3f, Mean: %.3f" % (std_dev, mean))

    # year = 2023
    # month = 3

    # df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    # df['prediction'] = y_pred

    # output_file = 'prediction.parquet'

    # df[['prediction', 'ride_id']].to_parquet(
    #     output_file,
    #     engine='pyarrow',
    #     compression=None,
    #     index=False
    # )
    # print('Data saved')


    # file_size_mb = get_file_size_in_mb(output_file)
    # print(f"{output_file} size: {file_size_mb:.2f} MB")

