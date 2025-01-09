# from flask import (
#     Flask,
#     request,
#     redirect,
#     url_for,
#     render_template_string,
#     session,
# )
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy(app)

# app = Flask(__name__)
# app.secret_key = "your_secrt_key"  # セッション管理のための秘密鍵

# # HTMLテンプレート
# base_template = """
# <!DOCTYPE html>
# <html lang="{{ lang }}">
# <head>
#     <meta charset="UTF-8">
#     <title>{{ title }}</title>
# </head>
# <body>
#     <h1>{{ greeting }}</h1>
#     <p>{{ instruction }}</p>
#     <form method="post" action="{{ url_for('set_language') }}">
#         <button type="submit" name="lang" value="ja">日本語</button>
#         <button type="submit" name="lang" value="en">English</button>
#     </form>
# </body>
# </html>
# """


# @app.route("/", methods=["GET"])
# def index():
#     # デフォルト言語は日本語
#     lang = session.get("lang", "ja")
#     texts = {
#         "ja": {
#             "title": "言語選択",
#             "greeting": "ようこそ",
#             "instruction": "表示言語を選択してください:",
#         },
#         "en": {
#             "title": "Language Selection",
#             "greeting": "Welcome",
#             "instruction": "Please select a language:",
#         },
#     }

#     # 選択された言語のテキストを表示
#     return render_template_string(
#         base_template,
#         **texts[lang],
#         lang=lang
#     )


# @app.route("/set_language", methods=["POST"])
# def set_language():
#     # ユーザーが選択した言語をセッションに保存
#     lang = request.form.get("lang")
#     if lang in ["ja", "en"]:
#         session["lang"] = lang
#     return redirect(url_for("index"))


# if __name__ == "__main__":
#     app.run(debug=True)