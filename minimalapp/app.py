from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate  import Migrate

db = SQLAlchemy()

def createapp():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = "ASMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pass@localhost/portal_db',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_ECHO = True,
        WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    )

    db.init_app(app)

    Migrate(app,db)

    #noticeアプリの登録とURLプレフィックス指定
    from notice import views as notice_views
    app.register_blueprint(notice_views.notice, url_prefix="/notice")

    #postアプリの登録とURLプレフィックス指定
    from post import views as post_views
    app.register_blueprint(post_views.post, url_prefix="/post")
    return app