from flask import Blueprint, render_template, redirect, url_for, Response, flash
from app import db
from minimalapp.notice.forms import NoticeUploadForm
from minimalapp.notice.models import Notice
from mimetypes import guess_type
#Bulueprintでnoticeアプリを生成する
notice = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

@notice.route("/")
def top():
    notices = Notice.query.all()
    return render_template("notice/top.html", notices=notices)
#住民投稿のエンドポイント
@notice.route("/create", methods=["GET","POST"])
def create_notice():
    #投稿フォームをインスタンス化
    form = NoticeUploadForm()
    
    if form.validate_on_submit():
        print("テスト")
        # ファイルデータをバイナリで取得
        image_data = None
        image_extension = None
        if form.image.data:
            image_file = form.image.data
            image_data = image_file.read()  # バイナリデータに変換
            # ファイルの拡張子を取得
            image_extension = image_file.filename.rsplit('.', 1)[-1].lower()  # 拡張子を取得

        #投稿を作成する 後でログインユーザーに直す
        notice = Notice(
            notice_title = form.title.data,
            notice_text = form.text.data,
            image = image_data,
            image_extension = image_extension,#拡張子を保存
            #tag = "テストタグ",
        )

        #お知らせ投稿を追加してコミットする
        db.session.add(notice)
        db.session.commit()
        return "投稿成功"
    
    return render_template("notice/create.html", form=form)

#画像表示確認のエンドポイント
@notice.route("/image/<int:notice_id>")
def get_image(notice_id):
    #取得出来たら画像の表示、出来なかったらエラーメッセージの表示
    notice = Notice.query.get_or_404(notice_id)
    if not notice.image:
        return "画像がありません", 404
    
    #print(f"画像データのサイズ: {len(post.image)} bytes")

    #画像の拡張子を取得
    mime_type, _ = guess_type(f"image.{notice.image_extension}")
    #mime_type = mime_type or "application/octet-stream"  # デフォルトのMIMEタイプ
    return Response(notice.image, mimetype=mime_type)

# お知らせ詳細
@notice.route("/detail/<int:notice_id>")
def detail(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    return render_template("notice/detail.html", notice=notice)

# お知らせ編集
@notice.route("/edit/<int:notice_id>", methods=["GET", "POST"])
def edit_notice(notice_id):
    notice = Notice.query.get_or_404(notice_id)
    form = NoticeUploadForm()

    if form.validate_on_submit():
        notice.notice_title = form.title.data
        notice.notice_text = form.text.data

        # 画像の更新処理
        if form.image.data:
            image_file = form.image.data
            notice.image = image_file.read()  # バイナリデータに変換
            notice.image_extension = image_file.filename.rsplit('.', 1)[-1].lower()  # 拡張子を取得

        db.session.commit()  # 変更をコミット
        return redirect(url_for('notice.edit_notice', notice_id=notice.notice_id))  # 更新後、編集ページを再読み込み

    # フォームの初期値に投稿データをセット
    form.title.data = notice.notice_title
    form.text.data = notice.notice_text
    # form.image.data = notice.image
    # form.image_extension = notice.image_extension

    return render_template("notice/edit.html", form=form, notice=notice)

# お知らせ削除
@notice.route('/<int:notice_id>/delete', methods=['POST'])
def delete(notice_id):
    # 削除処理
    notice = Notice.query.get(notice_id)
    if notice:
        db.session.delete(notice)
        db.session.commit()
    flash('お知らせを削除しました')
    return redirect(url_for('notice.top'))  # 削除が完了するとtopページに遷移
