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

#db.Modelを継承したPostreplyクラスを作成する
class Postreply(db.Model):
    #テーブル名を指定
    __tablename__="post_reply"
    #カラムの定義
    post_id = db.Column(db.Integer,)
    reply_id = db.Column(db.Integer,primary_key=True,)
    name = db.Column(db.String(10),)
    content = db.Column(db.Text)
