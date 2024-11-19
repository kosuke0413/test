from flask_wtf.file import FileAllowed, FileField
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms import StringField
from wtforms.validators import DataRequired,length
 
class AiForm(FlaskForm):

    text = StringField(
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
            FileAllowed("画像ファイルを指定してください"),
            FileAllowed(["png","jpg","jpeg"],
                        "サポートされていない画像形式です")
        ]
    )
 
    submit = SubmitField("アップロード")