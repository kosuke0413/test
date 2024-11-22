from flask_login import UserMixin
from werkzeug.security import generate_password
 
from app import db
 
 
class User(db.Model, UserMixin):
    __tablename__ = "users"
    local_id = db.Column(db.String(3),nullable=True)
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable=True)
    mailaddress = db.Column(db.String(50),nullable=True)
    password = db.Column(db.String(50),nullable=True)
 
    @property
    def password(self):
        raise AttributeError("読み取り不可")
   
    @password.setter
    def password(self, password):
        self.password = generate_password(password)
 
    # def verify_password(self, password):
    #     return check_password(self.password, password)
 
    def is_duplicate_mailadores(self):
        return User.query.filter_by(mailaddoress=self.mailaddoress).first() is not None