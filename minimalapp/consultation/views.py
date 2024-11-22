from flask import Blueprint, render_template, redirect, url_for, Response
from app import db
from minimalapp.consultation.forms import ConsultationForm
from minimalapp.consultation.models import Consultation
from mimetypes import guess_type

# Bulueprintでpostアプリを生成する
consultation = Blueprint(
    "consultation",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


@consultation.route("/")
def index():
    return "Hello consultation"


@consultation.route("/list", methods=["GET"])
def list():
    form = Consultation.query.all()
    return render_template("consultation/list.html", forms=form)


@consultation.route("/reply")
def reply():
    return render_template("consultation/reply.html")


# ゲットとポスト必須
@consultation.route("/send", methods=["GET", "POST"])
def send():
    # 緑文字がクラス
    form = ConsultationForm()
    if form.validate_on_submit():
        # 2は被らないため
        consultation2 = Consultation(
            # DBの名前つける
            title=form.title.data,
            content=form.content.data,
            mailadores="test",
            # 後から直す
        )

        db.session.add(consultation2)
        db.session.commit()
        # ドットつける
        return redirect(url_for("consultation.send_complate"))
    return render_template("consultation/send.html", form=form)
    # フォームに送るやよ


@consultation.route("send/send_complate")
def send_complate():
    return render_template("consultation/send_complate.html")
