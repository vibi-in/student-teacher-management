from flask import Blueprint, request, jsonify
from utils.db import get_connection

teachers_bp = Blueprint('teachers', __name__)

#For getting all teachers details
@teachers_bp.route('/teachers', methods=['GET'])
def view_teachers():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM students;")
        students = cursor.fetchall()
    return jsonify(students)

#For adding a new teacher
@teachers_bp.route('/teachers', methods=['POST'])
def add_teacher():
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO teachers (name, email) VALUES (%s, %s) RETURNING id;",
            (data['name'], data['email'])
        )
        conn.commit()
        student_id = cursor.fetchone()[0]
    return jsonify({"id": student_id}), 201

#For Updating teacher information
@teachers_bp.route('/teachers/<int:id>', methods=['PUT'])
def update_teacher(id):
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE teachers SET name=%s, email=%s WHERE id=%s;",
            (data['name'], data['email'], id)
        )
        conn.commit()
    return jsonify({"message": "Student updated"}), 200

#For Deletion of a teacher
@teachers_bp.route('/teachers/<int:id>', methods=['DELETE'])
def delete_teacher(id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM teachers WHERE id=%s;", (id,))
        conn.commit()
    return jsonify({"message": "Student deleted"}), 200

#For getting students for specific teacher
@teachers_bp.route('/teachers/<int:teacher_id>/students', methods=['GET'])
def get_students(teacher_id):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT students.* FROM students
            JOIN student_teacher ON student.id = student_teacher.student_id
            WHERE student_teacher.teacher_id = %s;
            """,
            (teacher_id,)
        )
        students = cursor.fetchall()
    return jsonify(students)