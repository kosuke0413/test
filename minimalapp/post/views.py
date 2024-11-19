from flask import Blueprint,render_template,redirect,url_for
from post.forms import PostUploadForm

#Bulueprintでpostアプリを生成する
post = Blueprint(
    "post",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

@post.route("/")
def index():
    return "Hello Posts"

@post.route("/upload", methods=["GET","POST"])
def create_post()
    #投稿フォームをインスタンス化
    form = PostUploadForm
    
    if form.validate_on_submit():
        #投稿を作成する