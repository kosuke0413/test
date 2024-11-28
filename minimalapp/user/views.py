from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from minimalapp.user.forms import SignUpForm,LoginForm
from minimalapp.user.models import User
from app import db

# 
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

# 新規登録のエンドポイント
@user.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            local_id=form.local_id.data,
            name=form.username.data,
            mailaddress=form.mailaddress.data,
        )
        user.password = form.password.data

        # 地域IDの存在チェック
        if not user.local_id_existence_confirmation():
            flash("指定の地域IDは存在しません")
            form.local_id.data = None
            return render_template("user/signup.html",form=form)
        
        # メールアドレス重複チェック
        if user.is_duplicate_mailaddress():
            flash("指定のメールアドレスは登録済みです")
            form.mailaddress.data = None
            return render_template("user/signup.html",form=form)


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
    
    return render_template("user/signup.html",form=form)


# ログイン機能のエンドポイント
@user.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(mailaddress=form.mailaddress.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("notice.top"))

        flash("メールアドレスかパスワードが不正です")
    
    return render_template("user/login.html",form=form)


@user.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("user.login"))