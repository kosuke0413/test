from flask import (
    Blueprint, render_template,
    redirect, url_for,
    Response, flash)
from app import db
from minimalapp.post.forms import PostUploadForm
from minimalapp.post.models import Post
from minimalapp.tags.models import Tags
from mimetypes import guess_type

# Bulueprintでpostアプリを生成する
post = Blueprint(
    "post",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


@post.route("/")
def index():
    return "Hello Posts"


# 住民投稿のエンドポイント
@post.route("/create", methods=["GET", "POST"])
def create_post():
    # 投稿フォームをインスタンス化
    form = PostUploadForm()

    if form.validate_on_submit():
        # ファイルデータをバイナリで取得
        image_data = None
        if form.image.data:
            image_file = form.image.data
            image_data = image_file.read()  # バイナリデータに変換
            # ファイルの拡張子を取得
            image_extension = image_file.filename.rsplit('.', 1)[-1].lower()
            # 拡張子を取得

            # 投稿を作成する 後でログインユーザーに直す
            post = Post(
                post_title=form.title.data,
                post_text=form.text.data,
                image=image_data,
                image_extension=image_extension,
                # 拡張子を保存
                tag=form.tag.data,
                name="テスト",
                local_id="a01"
            )

        else:
            # 投稿を作成する 後でログインユーザーに直す
            post = Post(
                post_title=form.title.data,
                post_text=form.text.data,
                tag=form.tag.data,
                name="テスト",
                local_id="a01"
            )

        # 住民投稿を追加してコミットする
        db.session.add(post)
        db.session.commit()
        return "投稿成功"

    return render_template("post/create.html", form=form)


# 画像表示確認のエンドポイント
@post.route("/image/<int:post_id>")
def get_image(post_id):
    # 取得出来たら画像の表示、出来なかったらエラーメッセージの表示
    post = Post.query.get_or_404(post_id)
    if not post.image:
        return "画像がありません", 404
    
    # print(f"画像データのサイズ: {len(post.image)} bytes")

    # 画像の拡張子を取得
    mime_type, _ = guess_type(f"image.{post.image_extension or 'jpeg'}")
    mime_type = mime_type or "application/octet-stream"  # デフォルトのMIMEタイプ
    return Response(post.image, mimetype=mime_type)


# 投稿一覧表示のエンドポイント
@post.route("/list")
def post_list():
    #投稿の一覧を取得、後で地域IDを指定するように変更
    posts = Post.query.all()
    return render_template("post/list.html", posts=posts)


# 投稿詳細表示のエンドポイント
@post.route("/detail/<int:post_id>")
def post_detail(post_id):
    #投稿と投稿に対応するタグを取得
    post = Post.query.get_or_404(post_id)
    tags = Tags.query.get_or_404(post.tag)
    return render_template("post/detail.html", post=post,tag=tags)


# 投稿編集のエンドポイント
@post.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostUploadForm()

    if form.validate_on_submit():
        post.post_title = form.title.data
        post.post_text = form.text.data

        # 画像の更新処理
        if form.image.data:
            image_file = form.image.data
            post.image = image_file.read()  # バイナリデータに変換
            post.image_extension = image_file.filename.rsplit(
                '.', 1)[-1].lower()  # 拡張子を取得

        db.session.commit()  # 変更をコミット
        return redirect(url_for('post.edit_post', post_id=post.post_id))
        # 更新後、編集ページを再読み込み

    # フォームの初期値に投稿データをセット
    form.title.data = post.post_title
    form.text.data = post.post_text
    #タグが設定されている場合は初期値をセット
    if post.tag == None:
        form.tag.data = str(post.tag)
    # form.image.data = notice.image
    # form.image_extension = notice.image_extension

    return render_template("post/edit.html", form=form, post=post)


# 投稿削除のエンドポイント
@post.route('/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
    # 削除処理
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    flash('お知らせを削除しました')
    return redirect(url_for('post.post_list'))  # 削除が完了するとtopページに遷移
