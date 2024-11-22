from app import db

# db.Modelを継承したPostクラスを作成する


class Consultation(db.Model):
    # テーブル名を指定
    __tablename__ = "consultation"

    # カラムの定義
    # id
    consult_id = db.Column(db.Integer, primary_key=True,)
    # title
    title = db.Column(db.String(30),)
    # 本文
    content = db.Column(db.Text,)
    # メールアドレス
    mailadores = db.Column(db.String(50),)
    # 地域ID
    local_id = db.Column(db.String(3), nullable=True)
