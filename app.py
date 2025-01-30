from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
import os
from flask_mail import Mail

# SQLAlchemyをインスタンス化
db = SQLAlchemy()
# Mailインスタンスを作成
mail = Mail()

# LoginManagerをインスタンス化
login_manager = LoginManager()
# 未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "user.login"
# ログイン後に表示するメッセージを表示
login_manager.login_message = ""


# アプリを生成
def createapp():
    app = Flask(__name__)
    # HTTPSを強制する設定
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    @app.route('/health', methods=['GET'])
    def health_check():
        return "Healthy", 200

    # エラーページ
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("error.html"), 404

    # テスト用のルート
    @app.route("/test-error")
    def test_404():
        return page_not_found(404)

    # メニューページ
    @app.route("/menu")
    @login_required
    def menu():
        # メニュー画面表示する関数に遷移
        return redirect(url_for("notice.menu"))

    # データベース設定
    app.config.from_mapping(
        SECRET_KEY="ASMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=(
            'postgresql://postgres:pass@localhost/portal_db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"
    )

    # login_managerをアプリと連携
    login_manager.init_app(app)
    # SQLAlchemyをアプリと連携
    db.init_app(app)
    # flask_migrateをアプリと連携
    Migrate(app, db)

    # noticeアプリの登録とURLプレフィックス指定
    from minimalapp.notice import views as notice_views
    app.register_blueprint(notice_views.notice)

    # postアプリの登録とURLプレフィックス指定
    from minimalapp.post import views as post_views
    app.register_blueprint(post_views.post, url_prefix="/post")

    # tagsアプリの登録とURLプレフィックス指定
    from minimalapp.tags import views as tags_views
    app.register_blueprint(tags_views.tags, url_prefix="/tags")

    # calendarアプリの登録とURLプレフィックス指定
    from minimalapp.calendar import views as calendar_views
    app.register_blueprint(calendar_views.Calen, url_prefix="/calendar")

    # 相談窓口アプリの登録とURLプレフィックス指定
    from minimalapp.consultation import views as consultation_views
    app.register_blueprint(consultation_views.consultation,
                           url_prefix="/consultation")

    # 翻訳アプリの登録とURLプレフィックス指定
    from minimalapp.translation import views as translation_views
    app.register_blueprint(translation_views.translation,
                           url_prefix="/translation")

    # ユーザーアプリの登録とURLプレフィックス指定
    from minimalapp.user import views as user_views
    app.register_blueprint(user_views.user, url_prefix="/user")

    # ユーザーアプリの登録とURLプレフィックス指定
    from minimalapp.ai import views as ai_views
    app.register_blueprint(ai_views.ai, url_prefix="/ai")

    # Mailクラスのコンフィグを追加する
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_POST"] = os.environ.get("MAIL_POST")
    app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

    # パスワードリセットトークンに使うソルト
    app.config["SECURITY_PASSWORD_SALT"] = 'salty_1414'

    # flask-mail拡張を登録する
    mail.init_app(app)

    return app
