from flask import Blueprint, render_template
from minimalapp.tags.models import Local
from flask_login import login_required, current_user

# Blueprintで言語選択アプリを生成
language = Blueprint(
    "language",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


@language.route("/translation")
def index():
    return render_template("translation/trans.html")


@language.context_processor
def inject_local():
    local = Local.query.get(current_user.local_id)
    return {
        "local": {"local_name": local.local_name}
    }
