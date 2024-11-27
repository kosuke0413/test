from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, length


class ConsultationForm(FlaskForm):
    # タイトルフィールドのバリデーションを設定
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルは必須です。"),
            length(max=30, message="30文字以内で入力してください。"),
        ]
    )
    # コメントフィールドのバリデーションを設定
    content = TextAreaField(
        "本文",
        validators=[
            DataRequired(message="本文は必須です。"),
            length(max=200, message="200文字以内で入力してください。"),
        ]
    )

    submit = SubmitField("アップロード")
