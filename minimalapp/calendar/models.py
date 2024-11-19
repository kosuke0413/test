from app import db

class Calendar(db.Model):
    __tablename__ = "calendar"
    calendar_id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    day = db.Column(db.Date, nullable=True)
