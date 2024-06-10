# Homework 04

```shell
pyenv install 3.10 && \
pyenv virtualenv 3.10 mlops-env
```

```shell
pip freeze | grep scikit=
```

```shell
source ~/.pyenv/versions/mlops-env/bin/activate
```

```shell
pip install --upgrade pip
```

```shell
jupyter notebook homework --ip 0.0.0.0 --port 8887 --NotebookApp.token='' --NotebookApp.password='' --allow-root --no-browser 
```


```shell
pip install pipenv
```

```shell
pipenv install  -r requirements.txt
```

```shell
jupyter nbconvert homework/starter.ipynb --to python --output prediction_script.py
```


```python
python prediction_script.py 2023 04 ~/Downloads/data
```

```shell
docker build -t mlops-deploy:latest -f Dockerfile homework
```

```shell
docker run -v "${HOME}/Downloads/data:/srv/data" -it mlops-deploy:latest
```

https://www.youtube.com/watch?v=18Lbaaeigek&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK

