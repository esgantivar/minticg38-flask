from flask import Flask, jsonify, request

from models.student import Student
from models.deparment import Department


app = Flask(__name__)


student = {
    "_id": 1,
    "cedula": "111111111",
    "first_name": "Pedro",
    "last_name": "Perez",
    "email": "pedro.perez@gmail.com"
}


@app.route("/", methods=["GET"])
def ping():
    return jsonify({
        "message": "Server running..."
    })

_students = [
        Student(
            _id=1,
            cedula="1111",
            first_name="pedro",
            last_name="perez",
            email="pedro.perez@gmail.com"
        ),
        Student(
            _id=2,
            cedula="1111",
            first_name="pedro",
            last_name="perez",
            email="pedro.perez@gmail.com"
        )
    ]


@app.route("/students", methods=["GET"])
def students():
    list_students = []
    for student in _students:
        list_students.append(student.__dict__)
    return jsonify({
        "students": list_students,
        "count": len(list_students)
    })


@app.route("/students/<int:id_student>", methods=["GET"])
def get_student_by_id(id_student):
    for student in _students:
        if student._id == id_student:
            return jsonify(student.__dict__)
    return jsonify({
        "error": "Not found"
    }), 404


@app.route("/students", methods=["POST"])
def create_student():
    """
    Crear un estudiante
    :return:
    """
    content = request.get_json()
    created_student = Student(
        _id=content["_id"],
        cedula=content["cedula"],
        first_name=content["first_name"],
        last_name=content["last_name"],
        email=content["email"]
    )
    _students.append(created_student)
    return jsonify({
        "message": "Estudiante fue creado de forma exitosa",
        "student": created_student.__dict__
    }), 201


@app.route("/students/<int:id_student>", methods=["PUT"])
def update_student(id_student):
    content = request.get_json()
    selected_student = None
    for _ in _students:
        if _._id == id_student:
            selected_student = _
    if not selected_student:
        return jsonify({
            "error": "Not found"
        }), 404

    selected_student.cedula = content["cedula"]
    selected_student.first_name = content["first_name"]
    selected_student.last_name = content["last_name"]
    selected_student.email = content["email"]

    return jsonify({
        "student": selected_student.__dict__
    })


@app.route("/students/<int:id_student>", methods=["DELETE"])
def delete_student(id_student):
    index = 0
    selected_index = -1
    for _ in _students:
        if _._id == id_student:
            selected_index = index
        index += 1

    if selected_index < 0 or selected_index >= len(_students):
        return jsonify({
            "error": "not found"
        }), 404
    _students.pop(selected_index)
    return jsonify({
        "message": f"El estudiante con id: {id_student} fue eliminado de forma exitosa"
    }), 200


app.run(host="127.0.0.1", port=5001, debug=True)
