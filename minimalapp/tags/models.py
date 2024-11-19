from app import db


class Tags(db.Model):
    __tablename__ = "tags"
    tag_id = db.Column(db.Integer, primary_key=True,nullable=True)
    tag_name = db.Column(db.String(50), nullable=True)


class Local(db.Model):
    __tablename__ = "local"
    local_id = db.Column(db.Integer, primary_key=True,)
    local_name = db.Column(db.String(20))
