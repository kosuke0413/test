from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from app import db

user = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="../static",
)


@user.route("/")
def index():
    return "Hello User"

# @user.route("/signup", methods=["GET","POST"])
# def signup():
#      form = SignUpForm()
#      if form.validate_on_submit():
#          user = SignUpForm(
#              local_id=form.lacal_id.date,
#              username=form.username.data,
#              mailadores=form.mailadores.data,
#              password=form.password.data,
#          )

#          if user.is_duplicate_mailadores():
#              flash("指定のメールアドレスは登録済みです")
#              return redirect(url_for("auth.signup"))

#          db.session.add(user)
#          db.session.commit()

#          login_user(user)

#          next_ = request.args.get("next")
#          if next_ is None or not next_.startswith("/"):
#              next_ = url_for("detector.index")
#          return redirect(next_)
    
#      return render_template("user/signup.html",form=form)


#  @auth.route("/login", methods=["GET","POST"])
#  def login():
#      form = LoginForm()
#      if form.validate_on_submit():
#          user = User.query.filter_by(mailadores=form.mailadores.data).first()

#          if user is not None and user.verify_password(form.password.data):
#              login_user(user)
#              return redirect(url_for("detector.index"))

#          flash("メールアドレスかパスワードが不正です")
    
#      return render_template("auth/login.html",form=form)


#  @auth.route("/logout")
#  def logout():
#      logout_user()    
#      return redirect(url_for("auth.login"))
