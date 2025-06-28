#!/bin/bash

print_slow() {
  local text="$1"
  local delay=${2:-0.05}  
  for ((i=0; i<${#text}; i++)); do
    echo -n "${text:$i:1}"
    sleep $delay
  done
  echo
}

check_error() {
  if [ $? -ne 0 ]; then
    echo -e "\e[31m❌ Ошибка: не удалось выполнить команду.\e[0m"
    exit 1
  fi
}

check_dir_created () {
  local folder=$1
  if [ -d "$folder" ]; then
    echo -e "📁 Папка \e[32m$folder\e[0m создана"
  else
    echo -e "❌ \e[31mОшибка:\e[0m папка $folder не создана"
    exit 1
  fi
}

### --- 1. Создание виртуального окружения --- ###
print_slow "🐍 Создание виртуального окружения..."
py -m venv venv
check_error
echo -e "✅ \e[32mВиртуальное окружение успешно создано!\e[0m"

### --- 2. Инициализация папок проекта --- ###
print_slow "📦 Создание необходимых папок..."
mkdir -p ./dags ./logs ./plugins ./config
touch .env
check_dir_created "./dags"
check_dir_created "./logs"
check_dir_created "./plugins"
check_dir_created "./config"

### --- 3. Заполнение .env файла --- ###
print_slow "📝 Заполнение .env файла..."
cat << EOF > .env
# UID пользователя, от имени которого запускается Airflow
AIRFLOW_UID=5000

# Настройки PostgreSQL
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
EOF
check_error
echo -e "✅ \e[32mФайл .env успешно создан!\e[0m"

### --- 4. Финальное сообщение --- ###
echo -e "\n🎉 \e[1;32mПроект успешно инициализирован!\e[0m"





