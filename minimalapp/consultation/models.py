from app import db

# db.Modelを継承したPostクラスを作成する


class Post(db.Model):
    # テーブル名を指定
    __tablename__ = "consultation"

    # カラムの定義
    # id
    consult_id = db.Column(db.Integer, primary_key=True,)
    # title
    title = db.Column(db.string(30),)
    # 本文
    content = db.Column(db.text(200),)
    # メールアドレス
    mailadores = db.Column(db.varchar(50),)
