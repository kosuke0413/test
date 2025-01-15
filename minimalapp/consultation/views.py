from flask import (Blueprint, render_template,
                   redirect, url_for, request,
                   flash)
from app import db
from minimalapp.consultation.forms import ConsultationForm
from minimalapp.consultation.models import Consultation
from flask_mail import Message
from app import mail
from minimalapp.tags.models import Local
from flask_login import login_required
from flask_login import current_user
from googletrans import Translator


# Bulueprintでpostアプリを生成する
consultation = Blueprint(
    "consultation",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


# 基礎
@consultation.route("/")
def index():
    catchphrase = 'なんて日だ！'

    translator = Translator()
    translated = translator.translate(catchphrase)
    print(translated.text)

    return translated.text


# 相談内容一覧
@consultation.route("/list", methods=["GET"])
@login_required
def list():
    # local とconsult のIDを取得して今後組み替える
    # Consultation クラスからDBの内容を all で全部持ってくる
    consul = Consultation.query.all()
    return render_template("consultation/list.html", consuls=consul)


# 相談に返信
@consultation.route("/reply<int:consult_id>", methods=['GET', 'POST'])
@login_required
def reply(consult_id):
    # Consultation クラスから consult_id だけを持ってきて consult に入れる
    consult = Consultation.query.get_or_404(consult_id)
    # consult を持ってく
    return render_template('consultation/reply.html',
                           consult=consult)


# お問い合わせ完了
@consultation.route("/reply/reply_complate")
@login_required
def reply_complate():
    return render_template("consultation/reply_complate.html")


# 質問の送信
@consultation.route("/send", methods=["GET", "POST"])
@login_required
def send():
    # 緑文字がクラス
    form = ConsultationForm()

    if current_user.manager_flag is True:
        return redirect(url_for("consultation.list"))

    if form.validate_on_submit():
        # 2は被らないため
        consultation2 = Consultation(
            # DBの名前つける
            title=form.title.data,
            content=form.content.data,
            # 届くメールアドレスの設定
            mailadores="kosuke.0413@icloud.com",
            # 後から直す
        )

        db.session.add(consultation2)
        db.session.commit()
        return redirect(url_for("consultation.send_complate"))
    return render_template("consultation/send.html", form=form)
    # フォームに送るやよ


# 送信完了ページ
@consultation.route("send/send_complate", methods=["GET", "POST"])
@login_required
def send_complate():
    if request.method == "POST":

        email = request.form.get("contact_mail")
        reply = request.form.get("reply")
        consult_id = request.form.get("consult_id")

        is_valid = True

        # 保留！！！！！！！！！！！！！！！！！！！
        # if not username:
        #     flash("ユーザ名は必須です")
        #     is_valid = False

        if not reply:
            flash("問い合わせ内容は必須です")
            is_valid = False

        # reply に飛ばす
        if not is_valid:
            return redirect(url_for("consultation.reply",
                                    consult_id=consult_id))

        # メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            reply=reply,
        )

        consult = Consultation.query.get_or_404(consult_id)
        db.session.delete(consult)
        db.session.commit()

        flash("問い合わせ内容はメールにて送信しました。問い合わせありがとうございます。")
        return redirect(url_for("consultation.reply_complate"))

    return render_template("consultation/send_complate.html")


# メールを送信する関数
def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


# ログインしたユーザーごとに町の名前の表示
@consultation.context_processor
def inject_local():
    local = Local.query.get(current_user.local_id)
    return {
        "local": {"local_name": local.local_name}
    }
