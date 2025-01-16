from flask import (Blueprint,
                   flash, redirect, render_template,
                   request, url_for, session)
from flask_login import login_user, logout_user, login_required
from minimalapp.user.forms import SignUpForm, LoginForm, LocalRegistForm
from minimalapp.user.models import User
from minimalapp.tags.models import Local
from app import db
from flask_login import current_user


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

@user.route("/profile_edit")
def profile_edit():
    return render_template("user/profile_edit.html")

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


@user.context_processor
def inject_local():
    # 未ログイン時は地域名を未定義にする
    if current_user.is_anonymous:
        return {"local": {"local_name": "未定義"}}

    local = Local.query.get(current_user.local_id)
    print(current_user.local_id)
    if local:
        return {
            "local": {"local_name": local.local_name}
        }

    else:
        return {"local": {"local_name": "未定義"}}
    
    
