from flask import Flask, jsonify
import psycopg2
import redis
import os

app = Flask(__name__)


def sql_init():
    sqls = [
        "CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY,name VARCHAR(50) NOT NULL);",
        "INSERT INTO test_table (name) VALUES ('Test Data 1'), ('Test Data 2');"
    ]
    conn = get_db_connection()
    cur = conn.cursor()
    for sql in sqls:        
        cur.execute(sql)        
    
    conn.commit()
    cur.close()    
    conn.close()
    print("------------------------sql-------------------")
    

# Подключение к PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="testdb",
        user="user",
        password="password"
    )
    return conn

# Подключение к Redis
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)

sql_init()

@app.route('/')
def index():
    # Проверяем кэш
    if cache.get('visits'):
        visits = int(cache.get('visits'))
    else:
        visits = 0

    # Увеличиваем счетчик посещений
    visits += 1
    cache.set('visits', visits)

    # Получаем данные из базы данных
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM test_table;')
    data = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({
        'visits': visits,
        'data': data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)