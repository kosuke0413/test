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
    from minimalapp.notice import views as notice_views
    app.register_blueprint(notice_views.notice)

    #postアプリの登録とURLプレフィックス指定
    from minimalapp.post import views as post_views
    app.register_blueprint(post_views.post, url_prefix="/post")

    #tagsアプリの登録とURLプレフィックス指定
    from minimalapp.tags import views as tags_views
    app.register_blueprint(tags_views.tags, url_prefix="/tags")

    #calendarアプリの登録とURLプレフィックス指定
    from minimalapp.calendar import views as calendar_views
    app.register_blueprint(calendar_views.calendar, url_prefix="/calendar")

    #相談窓口アプリの登録とURLプレフィックス指定
    from minimalapp.consultation import views as consultation_views
    app.register_blueprint(consultation_views.consultation, url_prefix="/consultaiton")

    return app