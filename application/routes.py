from flask import Blueprint, render_template
import db
import init

route_blueprint = Blueprint('route_blueprint', __name__)

@route_blueprint.route("/")
def index():
    return render_template("index.html")

@route_blueprint.route("/question")
def question():
    return db.get_random_question(init.r)

@route_blueprint.route("/question/<questionId>")
def question_by_id(questionId):
    return questionId

@route_blueprint.route("/report_question/<questionId>")
def report_shit_question(questionId):
    return db.report_shit_question(init.r, questionId)

@route_blueprint.route("/healthcheck")
def healthcheck():
    return "pong"

