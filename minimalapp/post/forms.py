from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms import StringField,TextAreaField
from wtforms.validators import DataRequired,length

class PostUploadForm(FlaskForm):
    #タイトルフィールドのバリデーションを設定
    title = StringField(
        "タイトル",
        validators=[
            DataRequired(message="タイトルは必須です。"),
            length(max=30,message="30文字以内で入力してください。"),
        ]
    )

    text = TextAreaField(
        "本文",
        validators=[
            DataRequired(message="本文は必須です。"),
            length(max=200,message="200文字以内で入力してください。"),
        ]     
    )
    #画像フィールドのバリデーションを設定
    image = FileField(
        "画像",
        validators=[
            FileAllowed(["png","jpg","jpeg"],
                        "サポートされていない画像形式です")
        ]
    )

    submit = SubmitField("アップロード")