from flask import jsonify, Blueprint

from controllers.registrations import RegistrationsController
from models.registration import RegistrationDoesNotExist

myself_bp = Blueprint("myself_registrations_bp", __name__)
registration_controller = RegistrationsController()


@myself_bp.route("<string:id_student>/registration", methods=["GET"])
def get_all(id_student):
    return jsonify({
        "registrations": [item.to_json() for item in registration_controller.get_by_student(id_student)]
    })


@myself_bp.route("<string:id_student>/registration/<string:id_registration>", methods=["GET"])
def get_by_id(id_student, id_registration):
    try:
        item = registration_controller.get_by_student_and_by_id(id_student, id_registration)
        return jsonify(item.to_json())
    except RegistrationDoesNotExist:
        return jsonify({
            "msg": "err"
        }), 404

