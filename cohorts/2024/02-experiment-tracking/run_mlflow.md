# MLFlow

Go to mlflow dir

```shell
cd cohorts/2024/02-experiment-tracking
```

```shell
make prepare-dirs
```

Build and up jupyter

```shell
docker-compose up mlflow-jupyter
```

```shell
cd src/jupyter_notebooks
```

```shell
python preprocess_data.py --raw_data_path /srv/data/trips --dest_path ./output
```

```shell
python train.py
```


```shell
python hpo.py
```

```shell
python register_model.py
```