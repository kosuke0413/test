from app import db

#db.Modelを継承したPostクラスを作成する
class Post(db.Model):
    #テーブル名を指定
    __tablename__="post"
    #カラムの定義
    post_id = db.Column(db.Integer, primary_key=True,)
    post_title = db.Column(db.String(30),)
    post_text = db.Column(db.String(200),)
    image = db.Column(db.LargeBinary)
    tag = db.Column(db.String(50),)
    name = db.Column(db.String(10), nullable=True)