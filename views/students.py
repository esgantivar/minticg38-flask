from flask import jsonify, request, Blueprint

from controllers.registrations import RegistrationsController
from controllers.students import StudentsController
from models.student import StudentDoesNotExist

students_controller = StudentsController()
registrations_controller = RegistrationsController()

students_bp = Blueprint("students_blueprint", __name__)


@students_bp.route("/", methods=["GET"])
def students():
    list_students = []
    for student in students_controller.get_all():
        list_students.append(student.__dict__)
    return jsonify({
        "students": list_students,
        "count": students_controller.count()
    })


@students_bp.route("/<string:id_student>", methods=["GET"])
def get_student_by_id(id_student):
    try:
        student = students_controller.get_by_id(id_student)
    except StudentDoesNotExist:
        return jsonify({
            "error": "El estudiante no existe"
        }), 404
    else:
        return jsonify(student.__dict__)


@students_bp.route("/", methods=["POST"])
def create_student():
    student = students_controller.create(request.get_json())
    return jsonify({
        "message": "Estudiante fue creado de forma exitosa",
        "student": student.__dict__
    }), 201


@students_bp.route("/<string:id_student>", methods=["PUT"])
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


@students_bp.route("/<string:id_student>", methods=["DELETE"])
def delete_student(id_student):
    try:
        result = students_controller.delete(id_student)
    except StudentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "message": "el estudiante fue borrado",
            "result": result
        }), 200


@students_bp.route("<string:id_student>/delete-registrations", methods=["DELETE"])
def delete_registrations_by_student(id_student):
    student = students_controller.get_by_id(id_student)
    return jsonify({
        "delete_count": registrations_controller.delete_by_student(student._id).deleted_count
    })


@students_bp.route("<string:id_student>/auth/<string:auth_id>", methods=["PUT"])
def assign_auth_id(id_student, auth_id):
    try:
        student = students_controller.assign_auth_id(id_student, auth_id)
    except StudentDoesNotExist:
        return jsonify({
            "msg": "Estudiante no existe"
        }), 404
    return jsonify({
        "student": student.to_json()
    })


@students_bp.route("/auth/<string:auth_id>", methods=["GET"])
def find_by_auth_id(auth_id):
    try:
        student = students_controller.get_by_auth_id(auth_id)
    except StudentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify(student.to_json()), 200
