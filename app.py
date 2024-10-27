from flask import Flask
from views.students import students_bp
from views.teachers import teachers_bp
from views.auth import auth_bp
from models import create_tables

app = Flask(__name__)

app.register_blueprint(students_bp)
app.register_blueprint(teachers_bp)
app.register_blueprint(auth_bp)

#For initialize Database Tables
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
