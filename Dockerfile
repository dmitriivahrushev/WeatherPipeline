FROM apache/airflow:2.10.5-python3.12
ADD req.txt .
RUN pip install -r req.txt