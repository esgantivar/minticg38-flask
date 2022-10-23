from flask import jsonify, Blueprint, request

from controllers.subjects import SubjectsController
from models.deparment import DepartmentDoesNotExist
from models.subject import SubjectDoesNotExist

subjects_bp = Blueprint("subjects_bp", __name__)

subject_controller = SubjectsController()


@subjects_bp.route("/", methods=["GET"])
def get_all():
    """
    subjects = []
    for item in subject_controller.get_all():
        subjects.append(item.to_json())
    """
    return jsonify({
        "subjects": [item.to_json() for item in subject_controller.get_all()]
    })


@subjects_bp.route("/", methods=["POST"])
def create():
    body = request.get_json()
    subject = subject_controller.create(body)
    return jsonify({
        "subject": subject.to_json()
    })


@subjects_bp.route("/<string:id_subject>", methods=["GET"])
def get_by_id(id_subject):
    try:
        student = subject_controller.get_by_id(id_subject)
    except SubjectDoesNotExist:
        return jsonify({
            "error": "La materia no existe"
        }), 404
    else:
        return jsonify(student.__dict__)


@subjects_bp.route("/<string:id_subject>", methods=["PUT"])
def update(id_subject):
    try:
        student = subject_controller.update(
            id_subject,
            request.get_json()
        )
    except SubjectDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "subject": student.__dict__
        })


@subjects_bp.route("/<string:id_subject>", methods=["DELETE"])
def delete(id_subject):
    try:
        result = subject_controller.delete(id_subject)
    except SubjectDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "message": "La materia fue borrada fue borrado",
            "result": result
        }), 200


@subjects_bp.route("/<string:id_subject>/department/<string:id_department>", methods=["PUT"])
def set_department_to_subject(id_subject, id_department):
    try:
        subject = subject_controller.set_department_to_subject(
            id_subject=id_subject,
            id_department=id_department
        )
        return jsonify({
            "message": "se asigno de forma exitosa",
            "subject": subject.to_json()
        })
    except SubjectDoesNotExist:
        return jsonify({
            "message": f"La materia con id: {id_subject} no existe"
        }), 400
    except DepartmentDoesNotExist:
        return jsonify({
            "message": f"El departamento con id: {id_department} no existe"
        }), 400
