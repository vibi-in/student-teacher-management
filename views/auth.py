from flask import Blueprint, request, jsonify, session
from utils.db import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

#For registering new student/teacher
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    designation = data['designation'].lower()
    
    with conn.cursor() as cursor:
        if designation == 'student':
            cursor.execute(
                "INSERT INTO students (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
                (data['name'], data['email'], hashed_password)
            )
        elif designation == 'teacher':
            cursor.execute(
                "INSERT INTO teachers (name, email, password) VALUES (%s, %s, %s) RETURNING id;",
                (data['name'], data['email'], hashed_password)
            )
        else:
            return jsonify({"message": "Invalid designation"}), 400

        conn.commit()
        user_id = cursor.fetchone()[0]
    return jsonify({"id": user_id}), 201

# Login a user
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    designation = data.get('designation', '').lower()
    
    with conn.cursor() as cursor:
        # Check the appropriate table based on designation
        if designation == 'student':
            cursor.execute("SELECT * FROM students WHERE email=%s;", (data['email'],))
        elif designation == 'teacher':
            cursor.execute("SELECT * FROM teachers WHERE email=%s;", (data['email'],))
        else:
            return jsonify({"message": "Invalid designation"}), 400

        user = cursor.fetchone()
        
        if user and check_password_hash(user[3], data['password']):  # Assuming password is in the 4th column
            session['user_id'] = user[0]
            session['designation'] = designation
            return jsonify({"message": "Login successful", "user_id": user[0], "name": user[1], "designation": designation})
        else:
            return jsonify({"message": "Invalid email or password"}), 401

# Logout a user
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('designation', None)
    return jsonify({"message": "Logout successful"}), 200
