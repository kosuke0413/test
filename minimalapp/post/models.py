from minimalapp.app import db

#db.Modelを継承したPostクラスを作成する
class Post(db.Model):
    #テーブル名を指定
    __tablename__="Post"
    #カラムの定義
    post_id = db.Column(db.Integer(10), primary_key=True, nullable=True)
    post_title = db.Column(db.String(30), nullable=True)
    post_text = db.Column(db.String(200), nullable=True)
    image = db.Column(db.LargeBinary)
    tag = db.Column(db.String(50),)
    name = db.Column(db.String(10), nullable=True)