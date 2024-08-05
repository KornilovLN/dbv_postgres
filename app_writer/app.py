from flask import Flask, request, jsonify, render_template_string
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>POST Request</title>
    </head>
    <body>
        <form id="postForm">
            <input type="text" name="name" value="KornilovLN StarmarkLN">
            <button type="submit">Send POST Request</button>
        </form>

        <script>
            document.getElementById('postForm').addEventListener('submit', function(event) {
                event.preventDefault();

                var formData = new FormData(event.target);
                var jsonData = JSON.stringify(Object.fromEntries(formData));

                fetch('/write', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: jsonData
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error));
            });
        </script>
    </body>
    </html>
    ''')

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
