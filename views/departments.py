from flask import jsonify, Blueprint, request

from controllers.departments import DepartmentsController
from models.deparment import DepartmentDoesNotExist

department_controller = DepartmentsController()
departments_bp = Blueprint("departments_blueprint", __name__)


@departments_bp.route("/", methods=["GET"])
def get_all_departments():
    departments = []
    for doc in department_controller.get_all():
        departments.append(doc.to_json())
    return jsonify({
        "departments": departments
    })


@departments_bp.route("/<string:id_department>", methods=["GET"])
def get_department_by_id(id_department):
    try:
        department = department_controller.get_by_id(id_department)
        return jsonify(department.to_json())
    except DepartmentDoesNotExist as e:
        return jsonify({
            "error": "el departamento no existe"
        }), 404


@departments_bp.route("/", methods=["POST"])
def create_department():
    department = department_controller.create(request.get_json())
    return jsonify({
        "message": "Departamento fue creado de forma exitosa",
        "department": department.to_json()
    }), 201


@departments_bp.route("/<string:id_department>", methods=["PUT"])
def update_department(id_department):
    try:
        department = department_controller.update(
            id_department,
            request.get_json()
        )
        return jsonify({
            "department": department.to_json()
        })
    except DepartmentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404


@departments_bp.route("/<string:id_department>", methods=["DELETE"])
def delete_department(id_department):
    try:
        result = department_controller.delete(id_department)
        return jsonify({
            "message": "el departamento fue borrado",
            "result": result
        }), 200
    except DepartmentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
