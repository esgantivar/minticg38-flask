from flask import Blueprint, jsonify, request

from controllers.departments import DepartmentsController
from controllers.departments import DepartmentDoesNotExist


departments_bp = Blueprint("departments_blueprint", __name__)
departments_controller = DepartmentsController()


@departments_bp.route("/", methods=["GET"])
def departments():
    list_departments = []
    for department in departments_controller.get_all():
        list_departments.append(department.to_json())
    return jsonify({
        "departments": list_departments,
        "count": departments_controller.count()
    })


@departments_bp.route("/<string:id_department>", methods=["GET"])
def get_department_by_id(id_department):
    try:
        department = departments_controller.get_by_id(id_department)
    except DepartmentDoesNotExist:
        return jsonify({
            "error": "El departamento no existe"
        }), 404
    else:
        return jsonify(department.__dict__)


@departments_bp.route("/", methods=["POST"])
def create_department():
    department = departments_controller.create(request.get_json())
    return jsonify({
        "message": "Departamento fue creado de forma exitosa",
        "department": department.__dict__
    }), 201


@departments_bp.route("/<string:id_department>", methods=["PUT"])
def update_department(id_department):
    try:
        department = departments_controller.update(
            id_department,
            request.get_json()
        )
    except DepartmentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "department": department.__dict__
        })


@departments_bp.route("/<string:id_department>", methods=["DELETE"])
def delete_department(id_department):
    try:
        result = departments_controller.delete(id_department)
    except DepartmentDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "message": "el departamento fue borrado",
            "result": result
        }), 200
