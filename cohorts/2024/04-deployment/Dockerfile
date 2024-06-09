FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

COPY prediction_script.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "prediction_script.py", "2023", "05", "/srv/data"]