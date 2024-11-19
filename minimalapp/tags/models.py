from app import db


class Tags(db.Model):
    __tablename__ = "tags"
    tag_id = db.Column(db.Integer(10), primary_key=True, nullable=True)
    tag_name = db.Column(db.String(50), nullable=True)


class Local(db.Model):
    __tablename__ = "local"
    local_id = db.Column(db.Integer(3), primary_key=True, nullable=True)
    local_name = db.Column(db.String(20))
