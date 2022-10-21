from flask import Flask, jsonify

from views.students import students_bp
from views.departments import departments_bp
from views.subjects import subjects_bp
from views.registrations import registrations_bp

app = Flask(__name__)


@app.route("/", methods=["GET"])
def ping():
    return jsonify({
        "message": "Server running..."
    })


app.register_blueprint(students_bp, url_prefix="/students")
app.register_blueprint(departments_bp, url_prefix="/departments")
app.register_blueprint(subjects_bp, url_prefix="/subjects")
app.register_blueprint(registrations_bp, url_prefix="/registrations")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
