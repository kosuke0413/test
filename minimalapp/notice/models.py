from app import db

# お知らせテーブル
class Notice(db.Model):
    __tablename__ = "notice"
    notice_id = db.Column(db.Integer, primary_key=True)
    notice_title = db.Column(db.String(30), nullable=False)
    notice_text = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    image_extension = db.Column(db.String(10))  # 画像の拡張子を保存するフィールド
    tag = db.Column(db.Integer, nullable=True)
    local_id = db.Column(db.String(3), nullable=True)


# お知らせ返信テーブル
class NoticeReply(db.Model):
    __tablename__ = "notice_reply"
    notice_id = db.Column(db.Integer, nullable=False) 
    reply_id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(10), nullable=False)       
    reply_text = db.Column(db.Text, nullable=False)