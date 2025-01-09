from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user,login_required
from minimalapp.user.forms import SignUpForm, LoginForm, LocalRegistForm
from minimalapp.user.models import User
from minimalapp.tags.models import Local
from app import db
from flask_login import login_required

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
@user.route("/signup", methods=["GET","POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            local_id=form.local_id.data,
            name=form.username.data,
            mailaddress=form.mailaddress.data,
            manager_flag = False
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
            # GETパラメータにnextキーが存在しない場合はトップページに遷移する
            next_ = request.args.get("next")
            if next_ is None or not next_.startswith("/"):
                next_ = url_for("notice.top")
            return redirect(next_)

        flash("メールアドレスかパスワードが不正です", "login_error")
    
    return render_template("user/login.html",form=form)


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


# 自治体ユーザーの新規登録のエンドポイント
@user.route("/signup_super", methods=["GET","POST"])
@login_required
def signup_super():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            local_id=form.local_id.data,
            name=form.username.data,
            mailaddress=form.mailaddress.data,
            manager_flag = True
        )
        user.password = form.password.data

        # 地域IDの存在チェック
        if not user.local_id_existence_confirmation():
            flash("指定の地域IDは存在しません")
            form.local_id.data = None
            return render_template("user/signup_super.html",form=form)
        
        # メールアドレス重複チェック
        if user.is_duplicate_mailaddress():
            flash("指定のメールアドレスは登録済みです")
            form.mailaddress.data = None
            return render_template("user/signup_super.html",form=form)


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
    
    return render_template("user/signup_super.html",form=form)


# 地域の新規登録のエンドポイント
@user.route("/local_regist", methods=["GET","POST"])
@login_required
def local_regist():
    form = LocalRegistForm()

    if form.validate_on_submit():
        local = Local(
            local_id = form.local_id.data,
            local_name = form.local_name.data
        )
        #地域id、地域名の重複チェック、後で書く

        
        # 地域情報を登録する
        db.session.add(local)
        db.session.commit()

        return "地域登録完了"

    return render_template("user/local_regist.html",form=form)