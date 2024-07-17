#!/bin/bash

# Чтение переменных окружения из .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Обновление списка пакетов и установка необходимых зависимостей
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev default-libmysqlclient-dev build-essential

# Установка pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.12 get-pip.py

# Установка и активация virtualenv
python3.12 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Предоставление прав пользователю MySQL
mysql -h"${DB_HOST}" -uroot -p"${DB_PASSWORD}" -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';"
mysql -h"${DB_HOST}" -uroot -p"${DB_PASSWORD}" -e "GRANT ALL PRIVILEGES ON *.* TO '${DB_USER}'@'%'; FLUSH PRIVILEGES;"

# Запуск tox
tox
