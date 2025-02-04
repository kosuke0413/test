from flask import (Blueprint, render_template, redirect, url_for,
                   Response, flash, session)
from app import db
from minimalapp.notice.forms import (NoticeUploadForm, NoticeReplyForm,
                                     SearchForm)
from minimalapp.notice.models import Notice, NoticeReply
from minimalapp.tags.models import Tags, Local
from mimetypes import guess_type
from sqlalchemy import or_
from flask_login import current_user, login_required


# Bulueprintでnoticeアプリを生成する
notice = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


@notice.route("/")
@login_required
def top():
    notices = Notice.query.filter(
        Notice.local_id == current_user.local_id).all()
    return render_template("notice/top.html", notices=notices)


# お知らせ投稿のエンドポイント
@notice.route("/create", methods=["GET", "POST"])
@login_required
def create_notice():
    # 投稿フォームをインスタンス化
    form = NoticeUploadForm()
    if form.validate_on_submit():
        # ファイルデータをバイナリで取得
        image_data = None
        image_extension = None
        if form.image.data:
            image_file = form.image.data
            image_data = image_file.read()  # バイナリデータに変換
            # ファイルの拡張子を取得
            image_extension = image_file.filename.rsplit('.', 1)[-1].lower()

        # 投稿を作成する 後でログインユーザーに直す
        notice = Notice(
            notice_title=form.title.data,
            notice_text=form.text.data,
            image=image_data,
            image_extension=image_extension,  # 拡張子を保存
            tag=form.tag.data,
            local_id=current_user.local_id
        )

        # お知らせ投稿を追加してコミットする
        db.session.add(notice)
        db.session.commit()
        return redirect(url_for("notice.top"))
    return render_template("notice/create.html", form=form)


# 画像表示確認のエンドポイント
@notice.route("/image/<int:notice_id>")
@login_required
def get_image(notice_id):
    # 取得出来たら画像の表示、出来なかったらエラーメッセージの表示
    notice = Notice.query.get_or_404(notice_id)
    if not notice.image:
        return "画像がありません", 404
    # print(f"画像データのサイズ: {len(post.image)} bytes")

    # 画像の拡張子を取得
    mime_type, _ = guess_type(f"image.{notice.image_extension}")
    # mime_type = mime_type or "application/octet-stream"  # デフォルトのMIMEタイプ
    return Response(notice.image, mimetype=mime_type)


# お知らせ詳細
@notice.route("/detail/<int:notice_id>")
@login_required
def detail(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    tags = None
    form = NoticeReplyForm()
    if notice.tag is not None:
        tags = Tags.query.get_or_404(notice.tag)
    replies = NoticeReply.query.filter_by(notice_id=notice_id).all()

    # # 投稿者の場合は編集画面にリダイレクト
    # if current_user.manager_flag:
    #     return redirect(url_for("notice.edit_notice", notice_id=notice_id))

    return render_template("notice/detail.html", notice=notice, tag=tags,
                           replies=replies, form=form)


# お知らせ編集
@notice.route("/edit/<int:notice_id>", methods=["GET", "POST"])
@login_required
def edit_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    form = NoticeUploadForm()

    if form.validate_on_submit():
        notice.notice_title = form.title.data
        notice.notice_text = form.text.data
        notice.tag = form.tag.data

        # 画像の更新処理
        if form.image.data:
            image_file = form.image.data
            notice.image = image_file.read()  # バイナリデータに変換
            notice.image_extension = image_file.filename.rsplit(
                '.', 1)[-1].lower()  # 拡張子を取得

        db.session.commit()  # 変更をコミット
        return redirect(url_for("notice.edit_notice",
                                notice_id=notice.notice_id))  # 更新後、編集ページを再読み込み

    # フォームの初期値に投稿データをセット
    form.title.data = notice.notice_title
    form.text.data = notice.notice_text
    if notice.tag is not None:
        form.tag.data = str(notice.tag)
    # form.image.data = notice.image
    # form.image_extension = notice.image_extension

    return render_template("notice/edit.html", form=form, notice=notice)


# お知らせ削除
@notice.route("/<int:notice_id>/delete", methods=["POST"])
@login_required
def delete(notice_id):
    # 削除したいnoticeを取得
    notice = Notice.query.get(notice_id)
    if notice:
        # まず関連するnotice_replyレコードを削除
        NoticeReply.query.filter_by(notice_id=notice_id).delete()

        # 次にnoticeレコードを削除
        db.session.delete(notice)
        db.session.commit()

    # お知らせトップページにリダイレクト
    return redirect(url_for('notice.top'))


# お知らせ返信
@notice.route("/reply/<int:notice_id>", methods=["GET", "POST"])
@login_required
def reply(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    form = NoticeReplyForm()

    if form.validate_on_submit():
        reply_text = form.text.data
        # 返信をデータベースに保存
        reply = NoticeReply(
            notice_id=notice_id,
            reply_text=reply_text,
            name=current_user.name
        )
        db.session.add(reply)
        db.session.commit()
        return redirect(url_for("notice.detail", notice_id=notice_id))
    return render_template("notice/reply.html", form=form, notice=notice)


# 返信削除処理
@notice.route("/reply/delete/<int:reply_id>", methods=["POST"])
@login_required
def reply_delete(reply_id):
    reply = NoticeReply.query.get_or_404(reply_id)
    notice_id = reply.notice_id

    # 返信削除
    db.session.delete(reply)
    db.session.commit()

    flash("返信を削除しました")
    return redirect(url_for("notice.detail", notice_id=notice_id))


# お知らせ検索
@notice.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        tag_id = form.tag.data
        if not tag_id:
            tag_id = None
        # 空白を削除
        notice_title = form.notice_title.data.strip()
        if not notice_title:
            notice_title = None

        # 検索クエリの生成
        query = db.session.query(Notice)
        local_id = session.get("local_id")  # ログイン時にセッションへ保存された地域コードを取得
        if local_id:
            query = query.filter(Notice.local_id == local_id)
        # タグまたはタイトルが指定されている場合
        if tag_id or notice_title:
            filters = []
            # .appendで末尾に追加
            if tag_id:
                filters.append(Notice.tag == tag_id)
            if notice_title:
                filters.append(Notice.notice_title.like(f"%{notice_title}%"))

            # OR 条件で検索
            # https://www.sukerou.com/2019/04/sqlalchemyandor.html
            query = query.filter(or_(*filters))
        # 結果を取得
        results = query.all()

        return render_template("notice/result.html", results=results)
    return render_template("notice/search.html", form=form)


# メニューページのエンドポイント
@notice.route("/menupage")
@login_required
def menu():
    return render_template("menu.html")


@notice.context_processor
def inject_local():
    # 地域がデータベースに存在しない場合は、地域名を未定義にする
    local = Local.query.get(current_user.local_id)
    if local:
        return {
            "local": {"local_name": local.local_name}
        }

    else:
        return {"local": {"local_name": "未定義"}}
