from flask import jsonify, Blueprint, request

from controllers.registrations import RegistrationsController
from models.registration import RegistrationDoesNotExist
from models.student import StudentDoesNotExist
from models.subject import SubjectDoesNotExist
from views.registrations.myself import myself_bp

registrations_bp = Blueprint("registrations_bp", __name__)
registration_controller = RegistrationsController()


@registrations_bp.route("/", methods=["GET"])
def get_all():
    return jsonify({
        "registrations": [item.to_json() for item in registration_controller.get_all()]
    })


@registrations_bp.route("/", methods=["POST"])
def create():
    try:
        registration = registration_controller.create(request.get_json())
        return jsonify(registration.to_json()), 201
    except StudentDoesNotExist:
        return jsonify({
            "message": f"el estudiante con id:... no existe"
        }), 400
    except SubjectDoesNotExist:
        return jsonify({
            "message": f"la materia no existe"
        }), 400


@registrations_bp.route("/<string:id_registration>", methods=["GET"])
def get_by_id(id_registration):
    try:
        registration = registration_controller.get_by_id(id_registration)
        return jsonify(registration.to_json())
    except RegistrationDoesNotExist:
        return jsonify({
            "message": "La inscripción no existe"
        }), 404


@registrations_bp.route("/<string:id_registration>", methods=["PUT"])
def update(id_registration):
    try:
        registration = registration_controller.update(id_registration, request.get_json())
        return jsonify(registration.to_json())
    except StudentDoesNotExist:
        return jsonify({
            "message": f"el estudiante con id:... no existe"
        }), 400
    except SubjectDoesNotExist:
        return jsonify({
            "message": f"la materia no existe"
        }), 400


@registrations_bp.route("/<string:id_registration>", methods=["DELETE"])
def delete(id_registration):
    try:
        return jsonify(registration_controller.delete(id_registration))
    except RegistrationDoesNotExist:
        return jsonify({
            "message": "inscripción no existe"
        })


@registrations_bp.route("/subject/<string:id_subject>/year/<int:year>/semester/<string:semester>", methods=["GET"])
def calc_avg_subject(id_subject, year, semester):
    return jsonify(list(registration_controller.calc_avg_subject(
        id_subject,
        year,
        semester
    )))


registrations_bp.register_blueprint(myself_bp, url_prefix="/student")

