from flask import (Blueprint,
                   flash, redirect, render_template,
                   request, url_for, session, current_app)
from flask_login import login_user, logout_user, login_required
from minimalapp.user.forms import (SignUpForm, LoginForm,
                                   ProfileForm, LocalRegistForm)
from minimalapp.user.models import User
from minimalapp.tags.models import Local
from app import db, mail
from flask_login import current_user
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from minimalapp.user.forms import ForgotPasswordForm, ResetPasswordForm


user = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="../static",
)


# テスト
@user.route("/")
def index():
    return "Hello User"


# 住民の新規登録のエンドポイント
@user.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            local_id=form.local_id.data,
            name=form.username.data,
            mailaddress=form.mailaddress.data,
            manager_flag=False
        )
        user.password = form.password.data

        # ユーザーがいない場合のみ、管理人フラグを付与
        if not User.query.filter_by(manager_flag=True).first():
            user.manager_flag = True

        # 地域IDの存在チェック
        if not user.local_id_existence_confirmation():
            flash("指定の地域IDは存在しません", "signup_error")
            form.local_id.data = None
            return render_template("user/signup.html", form=form)

        # メールアドレス重複チェック
        if user.is_duplicate_mailaddress():
            flash("指定のメールアドレスは登録済みです", "signup_error")
            form.mailaddress.data = None
            return render_template("user/signup.html", form=form)

        # ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()

        # ユーザー情報をセッションに登録する
        login_user(user)

        # GETパラメータにnextキーが存在しない場合はトップページに遷移する
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("notice.top")
        return redirect(next_)

    return render_template("user/signup.html", form=form)


# ログイン機能のエンドポイント
@user.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mailaddress=form.mailaddress.data).first()

        if user is not None and user.verify_password(form.password.data):
            session["local_id"] = user.local_id
            login_user(user)
            # GETパラメータにnextキーが存在しない場合はトップページに遷移する
            next_ = request.args.get("next")
            if next_ is None or not next_.startswith("/"):
                next_ = url_for("notice.top")
            return redirect(next_)

        flash("メールアドレスかパスワードが不正です", "login_error")

    return render_template("user/login.html", form=form)


# ログアウト機能のエンドポイント
@user.route("/logout")
def logout():
    logout_user()
    return render_template("user/logout.html")

    # # ユーザー削除
    # @user.route("/user/<int:user_id>/delete")
    # @login_required
    # def delete_user(user_id):
    #     user = User.query.filter_by(id=user_id).first().first()
    #     db.session.delete(user)
    #     db.session.commit()
    #     return "削除成功"


# マイページのエンドポイント
@user.route("/profile_edit", methods=["GET", "POST"])
@login_required
def profile_edit():
    form = ProfileForm()

    if form.validate_on_submit():
        # 自身を除いたメールアドレス重複チェック
        if User.query.filter(
            User.mailaddress == form.mailaddress.data,
            User.user_id != current_user.user_id  # 自身の user_id を除外
                ).first() is not None:
            flash("指定のメールアドレスは登録済みです", "profile")
            form.mailaddress.data = None
            return render_template("user/profile_edit.html", form=form)

        # 現在のユーザー情報を更新
        current_user.name = form.username.data
        current_user.mailaddress = form.mailaddress.data

        if form.password.data:
            current_user.password = form.password.data  # ハッシュ化済み

        # データベースに変更を保存
        db.session.commit()

        flash("プロフィール編集に成功しました。", "profile")

        # マイページにリダイレクト
        return redirect(url_for("user.profile_edit"))

    # 初期値をフォームに設定
    # ※パスワードは初期値をセット出来ない
    form.username.data = current_user.name
    form.mailaddress.data = current_user.mailaddress

    # マイページを表示
    return render_template("user/profile_edit.html", form=form)


# 自治体ユーザーの新規登録のエンドポイント
@user.route("/signup_super", methods=["GET", "POST"])
@login_required
def signup_super():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            local_id=form.local_id.data,
            name=form.username.data,
            mailaddress=form.mailaddress.data,
            manager_flag=True
        )
        user.password = form.password.data

        # # 管理人ユーザーがいない場合のみ、管理人フラグを付与
        # if not User.query.filter_by(manager_flag=True).first():
        #     user.manager_flag = True

        # 地域IDの存在チェック
        if not user.local_id_existence_confirmation():
            flash("指定の地域IDは存在しません", "signup_super_error")
            form.local_id.data = None
            return render_template("user/signup_super.html", form=form)

        # メールアドレス重複チェック
        if user.is_duplicate_mailaddress():
            flash("指定のメールアドレスは登録済みです", "signup_super_error")
            form.mailaddress.data = None
            return render_template("user/signup_super.html", form=form)

        # ユーザー情報を登録する
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("notice.top"))
    return render_template("user/signup_super.html", form=form)


# 自治体ユーザー一覧取得のエンドポイント
@user.route("/super_list")
@login_required
def super_list():
    # 自治体ユーザーをデータベースから取得
    users = db.session.query(User, Local).join(
        User, Local.local_id == User.local_id).filter(
            User.manager_flag == True)
    return render_template("user/super_list.html", users=users)

# 自治体ユーザー削除のエンドポイント
@user.route("/super_delete/<int:user_id>", methods=['POST'])
@login_required
def super_delete(user_id):
    # 自治体ユーザーの削除処理
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for("user.super_list"))


# 地域の新規登録のエンドポイント
@user.route("/local_regist", methods=["GET", "POST"])
@login_required
def local_regist():
    form = LocalRegistForm()

    if form.validate_on_submit():
        local = Local(
            local_id=form.local_id.data,
            local_name=form.local_name.data
        )

        # 地域idの重複チェック
        if Local.query.filter_by(local_id=local.local_id
                                 ).first() is not None:
            flash("地域IDが重複しています", "local_error")
            form.local_id.data = None
            return render_template("user/local_regist.html", form=form)

        # 地域名の重複チェック
        if Local.query.filter_by(local_name=local.local_name
                                 ).first() is not None:
            flash("地域名が重複しています", "local_error")
            form.local_name.data = None
            return render_template("user/local_regist.html", form=form)

        # 地域情報を登録する
        db.session.add(local)
        db.session.commit()

        return redirect(url_for("user.local_list"))

    return render_template("user/local_regist.html", form=form)


# 地域一覧のエンドポイント
@user.route("/local_list")
@login_required
def local_list():
    # 自治体ユーザーをデータベースから取得
    locals = db.session.query(Local).all()
    return render_template("user/local_list.html", locals=locals)


# 地域削除のエンドポイント
@user.route("/<local_id>/local_delete", methods=['POST'])
@login_required
def local_delete(local_id):
    # 地域の削除処理
    local = Local.query.get(local_id)
    if local:
        db.session.delete(local)
        db.session.commit()

        return redirect(url_for("user.local_list"))


# パスワードリセット要求のエンドポイント
@user.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(mailaddress=form.email.data).first()
        if user:
            # トークンを生成
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            token = serializer.dumps(user.mailaddress, salt=current_app.config['SECURITY_PASSWORD_SALT'])

            # パスワードリセットリンクを生成
            reset_url = url_for('user.reset_password',
                                token=token, _external=True)

            # メール送信（Flask-Mailを使用）
            msg = Message("パスワードリセット",
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[user.mailaddress])
            msg.body = f"以下のリンクからパスワードをリセットしてください:\n{reset_url}"
            mail.send(msg)

            flash("パスワードリセット用のリンクをメールで送信しました。", "info")
            return redirect(url_for('user.login'))

        flash("登録されていないメールアドレスです。", "error")

    return render_template("user/forgot_password.html", form=form)


# パスワードリセット処理を実行するエンドポイント
@user.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # トークンを検証して、メールアドレスを取得
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)  # 1時間で期限切れ
    except Exception as e:
        flash("無効なまたは期限切れのリンクです。", "error")
        return redirect(url_for('user.forgot_password'))

    # メールアドレスに対応するユーザーが存在しない場合
    user = User.query.filter_by(mailaddress=email).first()
    if not user:
        flash("このメールアドレスは登録されていません。", "error")
        return redirect(url_for('user.forgot_password'))

    # 新しいパスワードを設定するフォームを表示
    form = ResetPasswordForm()

    if form.validate_on_submit():
        # 新しいパスワードを設定
        user.password = form.password.data
        db.session.commit()

        flash("パスワードがリセットされました。ログインしてください。", "success")
        return redirect(url_for('user.login'))

    return render_template("user/reset_password.html", form=form)


@user.context_processor
def inject_local():
    # 未ログイン時は地域名を未定義にする
    if current_user.is_anonymous:
        return {"local": {"local_name": "未定義"}}

    local = Local.query.get(current_user.local_id)
    if local:
        return {
            "local": {"local_name": local.local_name}
        }

    else:
        return {"local": {"local_name": "未定義"}}

