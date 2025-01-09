from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from minimalapp.tags.models import Local

# Blueprintで言語選択アプリを生成
language = Blueprint(
    "language",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


# 言語選択画面の表示
@language.route('/trans', methods=['GET', 'POST'])
@login_required
def select_language():
    # サポートしている言語一覧
    supported_languages = {
        "en": "English",
        "ja": "日本語",
        "es": "Español",
        "fr": "Français"
    }

    if request.method == "POST":
        # ユーザーが選択した言語を取得
        selected_language = request.form.get("language")
        if selected_language in supported_languages:
            # セッションに保存
            session["language"] = selected_language
            flash(f"言語が {supported_languages[selected_language]} に変更されました。")
            return redirect(url_for("calendar.index"))  # 任意のリダイレクト先
        else:
            flash("選択した言語はサポートされていません。")
            return redirect(url_for("translation.select_language"))

    return render_template("translation/trans.html", languages=supported_languages)


@language.context_processor
def inject_local():
    local = Local.query.get(current_user.local_id)
    return {
        "local": {"local_name": local.local_name}
    }
