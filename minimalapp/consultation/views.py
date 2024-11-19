from flask import Blueprint,render_template

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
