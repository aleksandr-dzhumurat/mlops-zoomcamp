# Mage homework

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Q1: Mage version
v0.9.70

Q2
How many lines are in the created metadata.yaml file?
55



Q3
```shell
def ingest_files(**kwargs) -> pd.DataFrame:
    response = requests.get(
        'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'
    )

    if response.status_code != 200:
        raise Exception(response.text)

    df = pd.read_parquet(BytesIO(response.content))

    return df
```

http://localhost:6789/pipelines/taxi_data_preparing/edit?sideview=tree


A: 3403766

Q4: What's the size of the result?

A: 3,316,216

Q5: Train model
A: 24.77

Question 6. MLFlow
A: 4,534

