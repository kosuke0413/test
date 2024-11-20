from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, mailaddress, Length


class SignUpForm(FlaskForm):
    name = StringField(
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
            mailaddress(message="メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
            Length(1,50, message="50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("OK")


class LoginForm(FlaskForm):
    mailaddress = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Length(1,50, message="50文字以内で入力してください。"),
            mailaddress("メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
            Length(1,50, message="50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("OK")


