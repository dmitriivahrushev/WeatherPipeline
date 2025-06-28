# WeatherPipeline
![avatar](/image/weather_avatar.jpg)

### 🚀 О проекте  
В данном проекте осуществляется загрузка и обработка данных о погодных условиях в самых крупных городах России.  
Источник данных — WeatherAPI, предоставляющий актуальную информацию о погоде.  
Процесс автоматизирован с помощью оркестратора Apache Airflow, который управляет расписанием и контролем выполнения задач.  

### 📁 Структура проекта  
```
.
├── core/                # Вспомогательные функции.
├── dags/                # DAG.
├── image/               # Изображения.
├──.gitignore/           # Файлы, игнорируемые Git-ом.
├── docker-compose.yaml/ # Сервисы, необходимые для запуска проекта.
├── Dockerfile/          # Кастомная сборка.
├── README.md/           # Информация о проекте.
├── req.txt/             # Зависимости проекта.
└── init.sh              # Инициализация проекта.
```

### ⬇️ Запуск проекта
Запускаем **bash-скрипт** — он создаст виртуальное окружение и все необходимые папки для работы проекта.
~~~  
./setup_venv.sh
~~~

### 🆘 Ручная настройка (если возникли ошибки)  
Создайте файл `.env` со следующими переменными:  
```  
# UID пользователя, от имени которого запускается Airflow  
UID=5000  
# Настройки PostgreSQL  
POSTGRES_USER=airflow  
POSTGRES_PASSWORD=airflow  
POSTGRES_DB=airflow  
2. Создайте необходимые папки для Airflow:  
project_root/  
├── dags/  
├── logs/  
├── plugins/  
└── config/  
Эти папки требуются для корректной работы Airflow.  
```

### 🧩 Поднимаем Docker контейнеры
~~~
docker-compose -p weather_pipeline up -d
~~~

### 📂 Что нужно сделать в базе данных
#### 🔌 Подключение к базе данных `airflow`
```
Postgres:
  POSTGRES_USER: airflow
  POSTGRES_PASSWORD: airflow
  POSTGRES_DB: airflow
  ports:
    - 5422:5432
```
Создаём новую базу данных, выполнив скрипт:  
📄[DatabaseInit](/core/sql_scripts/database_init.sql)

#### 🌦️ Подключение к базе данных weather
```
postgres:
  POSTGRES_USER: airflow
  POSTGRES_PASSWORD: airflow
  POSTGRES_DB: weather
  ports:
    - 5422:5432
```
Выполняем скрипт инициализации таблиц:  
📄[TableInit](/core/sql_scripts/table_init.sql)

### 🌐 Настройка коннекторов в Airflow
Создаём подключение в **Airflow UI**:
- **Connection ID**: `http_conn_id`  
- **Connection Type**: `HTTP`  
- **Host**: `http://api.weatherapi.com/v1/current.json`  
- **Extra**:
  ```json
  {
    "api_token": "cbffd28e42404578a90182057252606"
  }

Создаём подключение в **Airflow UI**:  
-   **Connection ID**: `weather_conn`  
-   **Connection Type**: `Postgres`  
-  **Host**: postgres  
-  **Database**: weather  
-  **Login**: airflow  
-  **Pass**: airflow  
-  **Port**: 5432  

### 🔌 Доступные сервисы  
🗄️ База данных (PostgreSQL)  

    services: postgres_db
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    POSTGRES_DB: sprint_etl_db
    ports (локальный → контейнер): 5422:5432 

🌐 Airflow Web UI  

    User: airflow
    Pass: airflow
    ports (локальный → контейнер): 8080:8080


