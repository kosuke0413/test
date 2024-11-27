from flask import (Blueprint, render_template,
                   redirect, url_for, request,
                   flash)
from app import db
from minimalapp.consultation.forms import ConsultationForm
from minimalapp.consultation.models import Consultation
from email_validator import EmailNotValidError, validate_email
from flask_mail import Message
from app import mail

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
    consul = Consultation.query.all()
    return render_template("consultation/list.html", consuls=consul)


@consultation.route("/reply", methods=['GET', 'POST'])
def reply():
    # GETパラメータから取得
    title = request.args.get('title', '相談のタイトル')
    # GETパラメータから取得
    content = request.args.get('content', '相談内容の詳細')
    # title と content で情報を渡す
    contact_mail = request.args.get('contact_mail')

    return render_template('consultation/reply.html', title=title,
                           content=content, contact_mail=contact_mail)


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
            mailadores="kosuke.0413@icloud.com",
            # 後から直す
        )

        db.session.add(consultation2)
        db.session.commit()
        # ドットつける
        return redirect(url_for("consultation.send_complate"))
    return render_template("consultation/send.html", form=form)
    # フォームに送るやよ


@consultation.route("send/send_complate", methods=["GET", "POST"])
def send_complate():
    if request.method == "POST":

        # username = request.form["username"]
        email = request.form["contact_mail"]
        reply = request.form["reply"]


        # is_valid = True

        # if not username:
        #     flash("ユーザ名は必須です")
        #     is_valid = False

        # if not email:
        #     flash("メールアドレスは必須です")
        #     is_valid = False

        # try:
        #     validate_email(email)
        # except EmailNotValidError:
        #     flash("メールアドレスの形式で入力してください")
        #     is_valid = False

        if not reply:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("list"))

        # メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            # contact_mail=contact_mail,
            # username=username,
            reply=reply,
        )

        flash("問い合わせ内容はメールにて送信しました。問い合わせありがとうございます。")
        return redirect(render_template("consultation/reply_complate.html"))

    return render_template("consultation/send_complate.html")


def send_email(to, subject, template, **kwargs):
    # メールを送信する関数
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
