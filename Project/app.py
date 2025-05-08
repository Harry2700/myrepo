from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# PostgreSQL connection details
DB_HOST = "localhost"
DB_NAME = "mydatabase"
DB_USER = "your_user"
DB_PASSWORD = "your_password"

# Connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to a list of dictionaries
    users_list = [{'id': user[0], 'name': user[1], 'email': user[2]} for user in users]
    return jsonify(users_list)

if __name__ == '__main__':
    app.run(debug=True)
