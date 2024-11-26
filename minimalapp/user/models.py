from flask_login import UserMixin
from app import db,login_manager
from minimalapp.tags.models import Local
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"
    local_id = db.Column(db.String(3))
    user_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10))
    mailaddress = db.Column(db.String(50))
    password_hash = db.Column(db.String)


    # パスワードを読み取り不可に設定
    @property
    def password(self):
        raise AttributeError("読み取り不可")
    
    # パスワードのセッター
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # パスワードのチェック(ハッシュ値の一致確認)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # メッセージアドレス重複チェック
    def is_duplicate_mailaddress(self):
        return User.query.filter_by(mailaddress=self.mailaddress).first() is not None
    
    # 入力された地域IDが存在するか確認
    def local_id_existence_confirmation(self):
        return Local.query.filter_by(local_id=self.local_id).first() is not None
    
# ログインしているユーザー情報を取得する関数を作成する
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)