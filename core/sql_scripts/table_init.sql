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

COMMENT ON TABLE weather.public.current IS 'Данные о погоде в городах России';
COMMENT ON COLUMN public.current.id IS 'Уникальный идентификатор записи';
COMMENT ON COLUMN weather.public.current.city_name IS 'Город';
COMMENT ON COLUMN weather.public.current.region_name IS 'Регион';
COMMENT ON COLUMN weather.public.current.country IS 'Страна';
COMMENT ON COLUMN weather.public.current.location_time IS 'Текущее время';
COMMENT ON COLUMN weather.public.current.current_temp_c IS 'Температура воздуха в градусах Цельсия';
COMMENT ON COLUMN weather.public.current.current_temp_f IS 'Температура в градусах Фаренгейта';
COMMENT ON COLUMN weather.public.current.current_wind_mph IS 'Скорость ветра в милях в час';
COMMENT ON COLUMN weather.public.current.current_wind_kph IS 'Скорость ветра в километрах в час';
COMMENT ON COLUMN weather.public.current.current_wind_degree IS 'Направление ветра в градусах';
COMMENT ON COLUMN weather.public.current.current_wind_dir IS 'Кардинальное направление ветра (например, N, NW, SE)';