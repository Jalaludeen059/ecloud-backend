from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Database configuration
db = psycopg2.connect(
    host="localhost",
    database="ecloud",  # Your database name
    user="postgres",  # Your PostgreSQL username
    password="12345667"  # Your PostgreSQL password
)

cursor = db.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        active BOOLEAN NOT NULL DEFAULT TRUE
    );
""")

# CRUD Operations

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    active = data['active']

    cursor.execute("INSERT INTO users (username, password, active) VALUES (%s, %s, %s) RETURNING *", (username, password, active))
    user = cursor.fetchone()
    db.commit()
    return jsonify({'user': user})

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify({'users': users})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data['username']
    password = data['password']
    active = data['active']

    cursor.execute("UPDATE users SET username = %s, password = %s, active = %s WHERE id = %s RETURNING *", (username, password, active, user_id))
    user = cursor.fetchone()
    db.commit()
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)