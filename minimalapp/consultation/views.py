from flask import Blueprint, render_template

# Bulueprintでpostアプリを生成する
consultation = Blueprint(
    "consultation",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


@consultation.route("/")
def index():
    return "Hello consultation"


@consultation.route("/list")
def list():
    return render_template("consultation/list.html")


@consultation.route("/reply")
def reply():
    return render_template("consultation/reply.html")


@consultation.route("/send")
def send():
    return render_template("consultation/send.html")
