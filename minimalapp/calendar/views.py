from flask import Blueprint,render_template

#Blueprintでcalendarアプリを生成する
calendar = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

@calendar.route("/")
def index():
    return render_template("index.html")