from flask import Blueprint,render_template

#Bulueprintでpostアプリを生成する
post = Blueprint(
    "post",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

@post.route("/")
def index():
    return "Hello Posts"