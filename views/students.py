from flask import Blueprint, request, jsonify
from utils.db import get_connection

students_bp = Blueprint('students', __name__)

#For getting all students details
@students_bp.route('/students', methods=['GET'])
def get_students():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM students;")
        students = cursor.fetchall()
    return jsonify(students)

#For adding a new student
@students_bp.route('/students', methods=['POST'])
def add_student():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s) RETURNING id;",
            (data['name'], data['email'])
        )
        conn.commit()
        student_id = cursor.fetchone()[0]
    return jsonify({"id": student_id}), 201

#For Updating student information
@students_bp.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE students SET name=%s, email=%s WHERE id=%s;",
            (data['name'], data['email'], id)
        )
        conn.commit()
    return jsonify({"message": "Student updated"}), 200

#For Deletion of a student
@students_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM students WHERE id=%s;", (id,))
        conn.commit()
    return jsonify({"message": "Student deleted"}), 200

#For getting teachers for specific student
@students_bp.route('/students/<int:student_id>/teachers', methods=['GET'])
def get_teachers(student_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT teachers.* FROM teachers
            JOIN student_teacher ON teachers.id = student_teacher.teacher_id
            WHERE student_teacher.student_id = %s;
            """,
            (student_id,)
        )
        teachers = cursor.fetchall()
    return jsonify(teachers)