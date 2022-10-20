from flask import Blueprint, jsonify, request


from controllers.subject import SubjectsController
from models.subject import SubjectDoesNotExist

subjects_bp = Blueprint("subjects_blueprint", __name__)
subjects_controller = SubjectsController()


@subjects_bp.route("/", methods=["GET"])
def subjects():
    list_subjects = []
    for subject in subjects_controller.get_all():
        list_subjects.append(subject.to_json())
    return jsonify({
        "subjects": list_subjects,
        "count": subjects_controller.count()
    })


@subjects_bp.route("/<string:id_subject>", methods=["GET"])
def get_subject_by_id(id_subject):
    try:
        subject = subjects_controller.get_by_id(id_subject)
    except SubjectDoesNotExist:
        return jsonify({
            "error": "El materia no existe"
        }), 404
    else:
        return jsonify(subject.to_json())


@subjects_bp.route("/", methods=["POST"])
def create_subject():
    subject = subjects_controller.create(request.get_json())
    return jsonify({
        "message": "Departamento fue creado de forma exitosa",
        "subject": subject.__dict__
    }), 201


@subjects_bp.route("/<string:id_subject>", methods=["PUT"])
def update_subject(id_subject):
    try:
        subject = subjects_controller.update(
            id_subject,
            request.get_json()
        )
    except SubjectDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "subject": subject.__dict__
        })


@subjects_bp.route("/<string:id_subject>", methods=["DELETE"])
def delete_subject(id_subject):
    try:
        result = subjects_controller.delete(id_subject)
    except SubjectDoesNotExist:
        return jsonify({
            "error": "error"
        }), 404
    else:
        return jsonify({
            "message": "el materia fue borrado",
            "result": result
        }), 200
