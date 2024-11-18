from app import db


class Notice(db.Model):
    __tablename__ = "Notice"
    notice_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    tag = db.Column(db.String(50), nullable=True)
