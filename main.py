from flask import Flask, jsonify, request
from pymongo import MongoClient
from controllers.students import StudentsController, StudentDoesNotExist

from models.deparment import Department


app = Flask(__name__)

students_controller = StudentsController()


@app.route("/", methods=["GET"])
def ping():
    return jsonify({
        "message": "Server running..."
    })


@app.route("/students", methods=["GET"])
def students():
    list_students = []
    for student in students_controller.get_all():
        list_students.append(student.__dict__)
    return jsonify({
        "students": list_students,
        "count": students_controller.count()
    })


@app.route("/students/<int:id_student>", methods=["GET"])
def get_student_by_id(id_student):
    try:
        student = students_controller.get_by_id(id_student)
    except StudentDoesNotExist:
        return jsonify({
            "error": "El estudiante no existe"
        }), 404
    else:
        return jsonify(student.__dict__)


@app.route("/students", methods=["POST"])
def create_student():
    student = students_controller.create(request.get_json())
    return jsonify({
        "message": "Estudiante fue creado de forma exitosa",
        "student": student.__dict__
    }), 201


@app.route("/students/<int:id_student>", methods=["PUT"])
def update_student(id_student):
    try:
        student = students_controller.update(
            id_student,
            request.get_json()
        )
    except StudentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "student": student.__dict__
        })


@app.route("/students/<int:id_student>", methods=["DELETE"])
def delete_student(id_student):
    try:
        students_controller.delete(id_student)
    except StudentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "message": "el estudiante fue borrado"
        }), 200


MONGO_STRING_CONNECTION = "mongodb+srv://minticg38:ciclo4a2022@clusterg38.veo0jfn.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_STRING_CONNECTION)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
