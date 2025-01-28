from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# ユーザー新規登録機能のフォーム
class SignUpForm(FlaskForm):
    local_id = StringField(
        "地域ID",
        validators=[
            DataRequired(message="地域IDは必須です。"),
            Length(min=3, max=3, message="3文字で入力してください。"),
        ]
    )

    username = StringField(
        "名前",
        validators=[
            DataRequired(message="名前は必須です。"),
            Length(1, 10, message="10文字以内で入力してください。"),
        ],
    )

    mailaddress = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です。"),
            Length(1, 50, message="50文字以内で入力してください。"),
            Email(message="メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="パスワードは必須です。"),
            Length(4, 50, message="4文字以上、50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("登録")


# ログイン機能のフォーム
class LoginForm(FlaskForm):
    mailaddress = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Length(1, 50, message="50文字以内で入力してください。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
            Length(4, 50, message="4文字以上、50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("ログイン")


# プロフィール編集機能のフォーム
class ProfileForm(FlaskForm):
    username = StringField(
        "名前",
        validators=[
            DataRequired(message="名前は必須です。"),
            Length(1, 10, message="10文字以内で入力してください。"),
        ],
    )

    mailaddress = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"),
            Length(1, 50, message="50文字以内で入力してください。"),
            Email("メールアドレスの形式で入力してください。"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired("パスワードは必須です。"),
            Length(4, 50, message="4文字以上、50文字以内で入力してください。")
        ]
    )

    submit = SubmitField("プロフィール編集")


# 地域新規登録のフォーム
class LocalRegistForm(FlaskForm):
    local_id = StringField(
        "地域ID",
        validators=[
            DataRequired(message="地域IDは必須です。"),
            Length(min=3, max=3, message="3文字で入力してください。"),
        ]
    )

    local_name = StringField(
        "地域名",
        validators=[
            DataRequired(message="地域名は必須です。"),
        ]
    )

    submit = SubmitField("地域新規登録")


# メールアドレスの入力フォーム
class ForgotPasswordForm(FlaskForm):
    email = StringField('メールアドレス', validators=[
            DataRequired("メールアドレスは必須です。"),
            Length(1, 50, message="50文字以内で入力してください。"),
            Email("メールアドレスの形式で入力してください。"),
            ]
        )


# 新規パスワードの入力フォーム
class ResetPasswordForm(FlaskForm):
    password = PasswordField('新しいパスワード',
                             validators=[
                                DataRequired(message="パスワードは必須です。"),
                                Length(4, 50, message="4文字以上、50文字以内で入力してください。")
                                ]
                            )

    confirm_password = PasswordField('パスワード確認',
                                     validators=[
                                        DataRequired(message="パスワードは必須です。"),
                                        Length(4, 50, message="4文字以上、50文字以内で入力してください。"),
                                        EqualTo('password', message='パスワードが一致しません')
                                        ]
                                    )