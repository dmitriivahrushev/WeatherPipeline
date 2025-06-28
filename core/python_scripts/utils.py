from airflow.models.connection import Connection
from airflow.hooks.base import BaseHook
from airflow.providers.http.hooks.http import HttpHook
from collections.abc import MutableMapping
import psycopg
import requests
import humanize

def flatten(dictionary: dict, parent_key='', separator='_') -> dict:
    """
    flatten dict. Example: flatten({'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y' : 10}}, 'd': [1, 2, 3]}) ->
    {'a': 1, 'c_a': 2, 'c_b_x': 5, 'd': [1, 2, 3], 'c_b_y': 10}
    :param dictionary:
    :param parent_key: prefix for parent key
    :param separator: separator between keys
    :return: flatten dict
    """
    items = []
    for key, value in dictionary.items():
        new_key = parent_key + separator + key if parent_key else key
        if isinstance(value, MutableMapping):
            items.extend(flatten(value, new_key, separator=separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


def get_data(url: str, headers: dict[str, str], params: dict[str, str]) -> dict:
    """
    Base function to get data from generic API
    :param url:
    :param headers:
    :param params:
    :return: dict with all attributes API provides
    """
    params_to_display = {key: value for (key, value) in params.items() if
                         key.lower() not in ('key', 'api_key', 'token')}
    try:
        print(f"Start loading data from {url} with params: {params_to_display}")
        response = requests.get(
            url=url,
            headers=headers,
            params=params,
            verify=False
        )
        if response.status_code == 200:
            print("Data has been received")
            elapsed_seconds = response.elapsed.total_seconds()
            size = humanize.naturalsize(len(response.content))
            print(f"Time for download: {round(elapsed_seconds, 2)} seconds")
            print(f"Size of file: {size}")
            return response.json()
        else:
            response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        raise requests.exceptions.RequestException


def get_current_weather(city: str, aqi: str = 'no') -> dict:
    http_conn_id = HttpHook.get_connection('http_conn_id')
    api_token = http_conn_id.extra_dejson.get('api_token')
    wather_url = http_conn_id.host

    headers = {"Content-Type": "application/json; charset=utf-8"}
    
    paramas = {
        'key': api_token,
        'q': city,
        'aqi': aqi
    }
    data = get_data(
        url=wather_url,
        headers=headers,
        params=paramas
    )

    return data


def transform_weather_data(current_weather_dict: dict) -> dict:
    """
    Select required fields & rename
    :param current_weather_dict: dict with all attributes that API provides
    :return: dict with only required attributes
    """
    required_weather_params = [
        "location_name",
        "location_region",
        "location_country",
        "location_localtime",
        "current_temp_c",
        "current_temp_f",
        "current_wind_mph",
        "current_wind_kph",
        "current_wind_degree",
        "current_wind_dir"]
    mapping = {
        "location_name": "city_name",
        "location_region": "region_name",
        "location_country": "country",
        "location_localtime": "location_time",
    }
    required_fields = {key: value for (key, value) in flatten(current_weather_dict).items() if
                       key in required_weather_params}
    return {mapping[k] if k in mapping.keys() else k: v for k, v in required_fields.items()}


def get_conn_credentials(conn_id: str) -> Connection:
    """
    Function returns dictionary with connection credentials
    :param conn_id: str with airflow connection id
    :return: Connection
    """
    conn = BaseHook.get_connection(conn_id)
    return conn


def generate_insert_query(schema_name: str, table_name: str, data: dict) -> (str, list):
    """
    Generates insert query (PostgreSQL dialect) from the given params
    :param schema_name: schema name for insert query
    :param table_name:  table name for insert query
    :param data: dict of columns/data for insert query
    :return: query string ready to be inserted, values
    """

    columns = ", ".join(data.keys())
    values = tuple(data.values())

    placeholders = '%s, ' * (len(data.keys()) - 1) + '%s'
    query = f"INSERT INTO {schema_name}.{table_name} ({columns}) VALUES ({placeholders})"
    print(query)
    print(values)
    return query, values


def load_to_db(data: dict) -> None:
    """
    :param data: data to insert into PostgreSQL
    :return: None
    """
    pg_conn_credentials = get_conn_credentials('weather_conn')
    conn_dict = {
        'host': pg_conn_credentials.host,
        'port': pg_conn_credentials.port,
        'user': pg_conn_credentials.login,
        'password': pg_conn_credentials.password,
        'dbname': pg_conn_credentials.schema}

    with psycopg.connect(**conn_dict) as conn:
        with conn.cursor() as cursor:
            query, values = generate_insert_query(
                schema_name='public',
                table_name='current',
                data=data)
            cursor.executemany(query, [values])


def etl(**kwargs) -> None:
    city = kwargs['city']
    print('Start etl')
    for city_name in city:
        raw_data = get_current_weather(city=city_name)
        transformed_data = transform_weather_data(raw_data)
        load_to_db(transformed_data)
    print('etl finished')
