from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms import StringField,TextAreaField,RadioField
from wtforms.validators import DataRequired,length,Optional

class PostUploadForm(FlaskForm):
    # タイトルフィールドのバリデーションを設定
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルは必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ]
    )

    text = TextAreaField(
        "本文",
        validators=[
            DataRequired(message="本文は必須です。"),
            length(max=200, message="200文字以内で入力してください。"),
        ]
    )
    # 画像フィールドのバリデーションを設定
    image = FileField(
        "画像",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"],
                        "サポートされていない画像形式です")
        ]
    )

    # tagフィールド
    tag = RadioField(
        "タグ",
        choices=[
            ("1", "イベント・行事"),
            ("2", "子育て・教育"),
            ("3", "医療・健康"),
            ("4", "福祉・介護"),
            ("5", "ボランティア"),
            ("6", "注意喚起"),
        ],
        validators=[Optional()]
    )

    submit = SubmitField("アップロード")
