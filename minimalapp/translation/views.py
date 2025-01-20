from flask import Blueprint, render_template, request
from minimalapp.tags.models import Local
from flask_login import current_user
from googletrans import Translator

# Blueprintで言語選択アプリを生成
translation = Blueprint(
    "translation",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


# 翻訳ページへ飛ぶ
@translation.route("/translation", methods=["GET", "POST"])
def index():
    translated_text = ""
    if request.method == "POST":
        # 入力されたテキストとターゲット言語を取得
        text_to_translate = request.form.get("text_to_translate")
        target_language = request.form.get("target_language")
        if text_to_translate and target_language:
            # 翻訳を実行
            translator = Translator()
            translated = translator.translate(text_to_translate,
                                              dest=target_language)
            translated_text = translated.text
    return render_template("translation/translation.html",
                           translated_text=translated_text)


# ローカル関数の定義
@translation.context_processor
def inject_local():
    local = Local.query.get(current_user.local_id)
    return {
        "local": {"local_name": local.local_name}
    }
