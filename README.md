Создаем venv python 3.12



Init folders:
mkdir -p ./dags ./logs ./plugins ./config 
touch .env

# Создаем .env файл
AIRFLOW_UID=5000
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

Поднимаем Docker







Подключаемся к POSTGRES_DB: airflow
postgres:
    POSTGRES_USER: airflow
    POSTGRES_PASSWORD: airflow
    POSTGRES_DB: airflow
    ports:
    - 5422:5432
-- Создаем новую БД. CREATE DATABASE IF NOT EXISTS weather;


Подключаемся к POSTGRES_DB: weather
postgres:
    POSTGRES_USER: airflow
    POSTGRES_PASSWORD: airflow
    POSTGRES_DB: weather
    ports:
    - 5422:5432

-- Выполняем скрипт.
CREATE TABLE IF NOT EXISTS weather.public.current
(   id SERIAL PRIMARY KEY,
    city_name text,
    region_name text,
    country text,
    location_time timestamp,
    current_temp_c numeric,
    current_temp_f numeric,
    current_wind_mph numeric,
    current_wind_kph numeric,
    current_wind_degree int,
    current_wind_dir text
);

Создаем Connection в Ui airflow
http_conn_id
Connection Type * - HTTP
host = http://api.weatherapi.com/v1/current.json
Extra = {
  "api_token": "cbffd28e42404578a90182057252606"
}

Database conn 
Connection Id * - weather_conn
Connection Type * - Postgres
Host - Postgres 
Database - weather
Login - airflow
Port - 5432 

