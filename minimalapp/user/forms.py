from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# 新規登録機能のフォーム
class SignUpForm(FlaskForm):
    local_id =StringField(
        "地域ID",
        validators=[
            DataRequired(message="地域IDは必須です。"),
            Length(min=3,max=3, message="3文字で入力してください。"),
        ]
    )

    username = StringField(
        "名前",
        validators=[
            DataRequired(message="名前は必須です。"),
            Length(1,10, message="10文字以内で入力してください。"),
        ],
    )

    mailaddress = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Length(1,50, message="50文字以内で入力してください。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
            Length(1,50, message="50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("登録  ")

# ログイン機能のフォーム
class LoginForm(FlaskForm):
    mailaddress = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Length(1,50, message="50文字以内で入力してください。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
            Length(1,50, message="50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("ログイン")