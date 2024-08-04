## Writer (data generator, python) -> PostgreSQL <- Reader [data user, flask, python]

### <<< Создадим два контейнера Docker с приложениями на Python + Flask >>>
<br>которые будут общаться между собой через базу данных PostgreSQL.
<br>
#### В качестве примера создадим два приложения: одно будет записывать данные в базу данных, а другое читать их.

1. **_Шаг: Структура проекта_**

Создадим следующую структуру папок и файлов:
```
markdown

project/
│
├── docker-compose.yml
├── postgres/
│   └── Dockerfile
├── app_writer/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── app_reader/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```

2. **_Шаг: Конфигурация Docker Compose (docker-compose.yml)_**
```
yaml

version: '3.8'

services:
  postgres:
    image: postgres:latest
    container_name: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: exampledb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app_network

  app_writer:
    build: ./app_writer
    container_name: app_writer
    environment:
      DATABASE_URL: postgres://user:password@postgres:5432/exampledb
    depends_on:
      - postgres
    networks:
      - app_network

  app_reader:
    build: ./app_reader
    container_name: app_reader
    environment:
      DATABASE_URL: postgres://user:password@postgres:5432/exampledb
    depends_on:
      - postgres
    networks:
      - app_network

networks:
  app_network:
    driver: bridge

volumes:
  postgres_data:
```

3. **_Шаг: Dockerfile для PostgreSQL (postgres/Dockerfile)_**
<br>Для PostgreSQL мы будем использовать официальный образ - **postgres**

4. **_Шаг: Приложение Writer (app_writer/Dockerfile)_**
```
Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

5. **_Шаг: Приложение Writer (app_writer/requirements.txt)_**
```
text

Flask
psycopg2-binary
```

6. **_Шаг 6: Приложение Writer (app_writer/app.py)_**
```
python

from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/write', methods=['POST'])
def write():
    data = request.json
    name = data.get('name')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name) VALUES (%s)', (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

7. **_Шаг: Приложение Reader (app_reader/Dockerfile)_**
```
Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

8. **_Шаг: Приложение Reader (app_reader/requirements.txt)_**
```
text

Flask
psycopg2-binary
```

9. **_Шаг: Приложение Reader (app_reader/app.py)_**
```
python

from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/read', methods=['GET'])
def read():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

10. **_Шаг: Создание таблицы в базе данных_**
<br>Перед запуском контейнеров, создадим таблицу users в базе данных PostgreSQL.
<br>Можно сделать это с помощью следующего скрипта:
```
sql

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
```

Запустите контейнер PostgreSQL, затем подключитесь к нему и выполните этот SQL-скрипт.

11. **_Шаг 11: Запуск Docker Compose_**
<br>Теперь, когда все файлы созданы, можно запустить docker-compose для развертывания приложений:
```
bash

docker-compose up --build
```

12. **_Шаг 12: Тестирование_**
<br>Теперь вы можете использовать curl или Postman для тестирования работы ваших приложений.

**_Для записи данных:_**
```
    bash

curl -X POST http://localhost:5000/write -H "Content-Type: application/json" -d '{"name": "John Doe"}'
```

**_Для чтения данных:_**
```
bash

    curl http://localhost:5001/read
```

<<< **Два контейнера с приложениями на Python + Flask общаются через базу данных PostgreSQL** >>>

#-----------------------------------------------------
```
Подключиться к контейнеру PostgreSQL и создать таблицу можно следующим образом:
Шаг 1: Запустите контейнер PostgreSQL

Убедитесь, что ваш docker-compose.yml файл правильно настроен, и запустите контейнеры:

bash

docker-compose up -d

Шаг 2: Подключение к контейнеру PostgreSQL

Теперь подключитесь к контейнеру PostgreSQL с помощью Docker. Для этого используйте следующую команду:

bash

docker exec -it postgres psql -U user -d exampledb

Здесь:

    postgres — имя контейнера.
    psql — клиентская утилита PostgreSQL для работы с базой данных.
    -U user — флаг для указания пользователя (в нашем случае это user).
    -d exampledb — флаг для указания базы данных (в нашем случае это exampledb).

Шаг 3: Создание таблицы

После выполнения предыдущей команды вы окажетесь в интерактивной оболочке PostgreSQL. Выполните следующий SQL-запрос для создания таблицы users:

sql

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

Полный процесс в терминале

    Запустите контейнеры в фоновом режиме:

    bash

docker-compose up -d

Подключитесь к контейнеру PostgreSQL:

bash

docker exec -it postgres psql -U user -d exampledb

В интерактивной оболочке PostgreSQL выполните команду создания таблицы:

sql

    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );

Проверка таблицы

Чтобы убедиться, что таблица создана правильно, можно выполнить команду:

sql

\d users

Это покажет структуру таблицы users.

После этих шагов ваша база данных PostgreSQL будет готова к использованию двумя приложениями Flask для записи и чтения данных.
```