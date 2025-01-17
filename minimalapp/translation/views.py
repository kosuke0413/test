from flask import Blueprint, render_template
from minimalapp.tags.models import Local
from flask_login import current_user

# Blueprintで言語選択アプリを生成
translation = Blueprint(
    "translation",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


@translation.route("/translation")
def index():
    return render_template("translation/translation.html")


@translation.context_processor
def inject_local():
    local = Local.query.get(current_user.local_id)
    return {
        "local": {"local_name": local.local_name}
    }
