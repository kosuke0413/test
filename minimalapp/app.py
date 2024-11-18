from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def createapp():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="ASMss3p5QPbcY2hBsJ",
        SQLALCEMY_DATABACE_URI='postgresql//postgres:pass@localhost/portal_db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"
    )

    db.init_app(app)

    Migrate(app, db)
    return app
