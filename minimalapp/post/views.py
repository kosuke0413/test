from flask import (
    Blueprint, render_template,
    redirect, url_for,
    Response, session)
from app import db
from minimalapp.post.forms import PostUploadForm, PostReplyForm, SearchPostForm
from minimalapp.post.models import Post, Postreply
from minimalapp.tags.models import Tags, Local
from minimalapp.user.models import User
from mimetypes import guess_type
from sqlalchemy import or_
from flask_login import current_user, login_required

# Bulueprintでpostアプリを生成する
post = Blueprint(
    "post",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


# 住民投稿のエンドポイント
@post.route("/create", methods=["GET", "POST"])
@login_required
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
                user_id=current_user.user_id,
                local_id=current_user.local_id
            )

        else:
            # 投稿を作成する 後でログインユーザーに直す
            post = Post(
                post_title=form.title.data,
                post_text=form.text.data,
                tag=form.tag.data,
                user_id=current_user.user_id,
                local_id=current_user.local_id
            )

        # 住民投稿を追加してコミットする
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.post_list'))

    return render_template("post/create.html", form=form)


# 画像表示確認のエンドポイント
@post.route("/image/<int:post_id>")
@login_required
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
@login_required
def post_list():
    # 投稿の一覧を取得、後で地域IDを指定するように変更
    posts = Post.query.filter(Post.local_id == current_user.local_id).all()
    return render_template("post/list.html", posts=posts)


# 投稿詳細表示のエンドポイント
@post.route("/detail/<int:post_id>")
@login_required
def post_detail(post_id):
    # 投稿と投稿に対応するタグを取得
    post = Post.query.get_or_404(post_id)
    tags = None
    # if not post.tag == None: どちらか
    if post.tag is not None:
        tags = Tags.query.get_or_404(post.tag)
    # 対応する返信を取得
    replies = Postreply.query.filter_by(post_id=post_id)
    # 投稿ユーザー情報を取得
    user = User.query.get_or_404(post.user_id)

    # # 投稿者の場合は編集画面を表示
    # if user.user_id == current_user.user_id:
    #     return edit_post(post_id)

    return render_template("post/detail.html", post=post, tag=tags,
                           replies=replies, user=user)


# 投稿編集のエンドポイント
@post.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostUploadForm()

    if form.validate_on_submit():
        post.post_title = form.title.data
        post.post_text = form.text.data
        post.tag = form.tag.data

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
    # タグが設定されている場合は初期値をセット
    # if not post.tag == None: どちらか
    if post.tag is not None:
        form.tag.data = str(post.tag)
    # form.image.data = notice.image
    # form.image_extension = notice.image_extension

    return render_template("post/edit.html", form=form, post=post,
                           post_id=post_id)


# 投稿削除のエンドポイント
@post.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    # 削除したいpostを取得
    post = Post.query.get(post_id)
    
    if post:
        # まず関連するpost_replyレコードを削除
        Postreply.query.filter_by(post_id=post_id).delete()

        # 次にpostレコードを削除
        db.session.delete(post)
        db.session.commit()

    # 投稿一覧ページにリダイレクト
    return redirect(url_for('post.post_list'))


# 投稿返信
@post.route("/reply/<int:post_id>", methods=["GET", "POST"])
@login_required
def reply(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostReplyForm()

    if form.validate_on_submit():
        reply_text = form.text.data
        # 返信をデータベースに保存
        reply = Postreply(
            post_id=post_id,
            content=reply_text,
            name=current_user.name
        )
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for("post.post_detail", post_id=post_id))
    return render_template("post/reply.html", form=form, post=post)


# 返信削除処理
@post.route("/reply/delete/<int:reply_id>", methods=["POST"])
@login_required
def reply_delete(reply_id):
    reply = Postreply.query.get_or_404(reply_id)
    post_id = reply.post_id

    # 返信削除
    db.session.delete(reply)
    db.session.commit()

    # flash("返信を削除しました")
    return redirect(url_for("post.post_detail", post_id=post_id))


# 投稿検索
@post.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchPostForm()
    if form.validate_on_submit():
        tag_id = form.tag.data
        if not tag_id:
            tag_id = None
        # 空白を削除
        post_title = form.post_title.data.strip()
        if not post_title:
            post_title = None

        # 検索クエリの生成
        query = db.session.query(Post)
        local_id = session.get("local_id")  # ログイン時にセッションへ保存された地域コードを取得
        if local_id:
            query = query.filter(Post.local_id == local_id)

        # タグまたはタイトルが指定されている場合
        if tag_id or post_title:
            filters = []
            # .appendで末尾に追加
            if tag_id:
                filters.append(Post.tag == tag_id)
            if post_title:
                filters.append(Post.post_title.like(f"%{post_title}%"))

            # OR 条件で検索
            query = query.filter(or_(*filters))
            # https://www.sukerou.com/2019/04/sqlalchemyandor.html

        # 結果を取得
        results = query.all()

        return render_template("post/result.html", results=results)
    return render_template("post/search.html", form=form)


@post.context_processor
def inject_local():
    # 地域がデータベースに存在しない場合は、地域名を未定義にする
    local = Local.query.get(current_user.local_id)
    if local:
        return {
            "local": {"local_name": local.local_name}
        }

    else:
        return {"local": {"local_name": "未定義"}}
