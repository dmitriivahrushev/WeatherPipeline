-- Создаем новую БД.
CREATE DATABASE IF NOT EXISTS weather;

-- Подключаемся к новой БД weather и выполняем скрипт.
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
    current_wind_dir text,
    CONSTRAINT unique_city_time UNIQUE (city_name, location_time)
);