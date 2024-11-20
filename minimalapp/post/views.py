from flask import Blueprint,render_template,redirect,url_for,Response
from app import db
from minimalapp.post.forms import PostUploadForm
from minimalapp.post.models import Post
from mimetypes import guess_type

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

#住民投稿のエンドポイント
@post.route("/create", methods=["GET","POST"])
def create_post():
    #投稿フォームをインスタンス化
    form = PostUploadForm()
    
    if form.validate_on_submit():
        # ファイルデータをバイナリで取得
        image_data = None
        if form.image.data:
            image_file = form.image.data
            image_data = image_file.read()  # バイナリデータに変換
            # ファイルの拡張子を取得
            image_extension = image_file.filename.rsplit('.', 1)[-1].lower()  # 拡張子を取得

        #投稿を作成する 後でログインユーザーに直す
        post = Post(
            post_title = form.title.data,
            post_text = form.text.data,
            image = image_data,
            image_extension = image_extension,#拡張子を保存
            tag = "テストタグ",
            name = "テスト",
        )

        #住民投稿を追加してコミットする
        db.session.add(post)
        db.session.commit()
        return "投稿成功"
    
    return render_template("post/create.html", form=form)

#画像表示確認のエンドポイント
@post.route("/image/<int:post_id>")
def get_image(post_id):
    #取得出来たら画像の表示、出来なかったらエラーメッセージの表示
    post = Post.query.get_or_404(post_id)
    if not post.image:
        return "画像がありません", 404
    
    print(f"画像データのサイズ: {len(post.image)} bytes")

    #画像の拡張子を取得
    mime_type, _ = guess_type(f"image.{post.image_extension or 'jpeg'}")
    mime_type = mime_type or "application/octet-stream"  # デフォルトのMIMEタイプ
    return Response(post.image, mimetype=mime_type)