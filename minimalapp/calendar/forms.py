from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms import StringField, TextAreaField, DateField
from wtforms.validators import DataRequired, length


class CalendarregistForm(FlaskForm):

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

    date = DateField(
       "日付",
       validators=[
           DataRequired(message="日付は必須です。"),
       ]
    )

    submit = SubmitField("登録")
