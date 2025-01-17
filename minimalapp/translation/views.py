from flask import Blueprint


# Blueprintで言語選択アプリを生成
translation = Blueprint(
    "translation",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

@translation.route("/")
def index():
    return "Hello world"
