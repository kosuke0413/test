from flask_login import UserMixin
#from werkzeug.security import check_password, generate_password
 
from app import db
 
 
class User(db.Model, UserMixin):
    __tablename__ = "users"
    local_id = db.Column(db.String(3),nullable=True)
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),nullable=True)
    mailaddress = db.Column(db.String(50),nullable=True)
    password = db.Column(db.String(50),nullable=True)
 
    # @property
    # def pasword(self):
    #     raise AttributeError("読み取り不可")
   
    # @password.setter
    # def pasword(self, password):
    #     self.pasword = generate_password(password)
 
    # def verify_pasword(self, password):
    #     return check_password(self.pasword, password)
 
    # def is_duplicate_mailadores(self):
    #     return User.query.filter_by(mailaddoress=self.mailaddoress).first() is not None