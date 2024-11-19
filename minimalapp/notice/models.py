from app import db

# お知らせテーブル
class Notice(db.Model):
    __tablename__ = "notice"
    notice_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    tag = db.Column(db.String(50), nullable=True)


# お知らせ返信テーブル
class NoticeReply(db.Model):
    __tablename__ = "reply"
    notice_id = db.Column(db.Integer, nullable=False) 
    reply_id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(10), nullable=False)       
    content = db.Column(db.Text, nullable=False)