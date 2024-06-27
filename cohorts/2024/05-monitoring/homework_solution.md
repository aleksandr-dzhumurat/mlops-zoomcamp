# Homework 05

```shell
cd /Users/username/PycharmProjects/mlops-zoomcamp/05-monitoring
```

```shell
pyenv install 3.10 && \
pyenv virtualenv 3.10 evidently-env
```


```shell
source ~/.pyenv/versions/evidently-env/bin/activate
```

```shell
pip install --upgrade pip
```

```shell
pip install  -r requirements.txt
```

```shell
jupyter notebook
 . --ip 0.0.0.0 --port 8887 --NotebookApp.token='' --NotebookApp.password='' --allow-root --no-browser
```

Q2

Run monitoring

```shell
python evidently_metrics_calculation_homework.py
```



[Saving Dashboards](https://youtu.be/-c4iumyZMyw?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&t=202)
