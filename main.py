from dotenv import load_dotenv
from flask import Flask, jsonify

from controllers.students import StudentsController
from views.department import departments_bp
from views.student import students_bp
from views.subject import subjects_bp

load_dotenv()

app = Flask(__name__)

students_controller = StudentsController()


@app.route("/", methods=["GET"])
def ping():
    return jsonify({
        "message": "Server running..."
    })


app.register_blueprint(students_bp, url_prefix="/student")
app.register_blueprint(departments_bp, url_prefix="/department")
app.register_blueprint(subjects_bp, url_prefix="/subjects")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
