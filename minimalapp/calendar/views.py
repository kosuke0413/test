from flask import Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, date
import calendar
from minimalapp.calendar.forms import CalendarregistForm
from minimalapp.calendar.models import Calendar
from app import db
from sqlalchemy import select

# Blueprintでcalendarアプリを生成する
Calen = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

# 月の開始日と終了日を取得する関数
# def get_month_range(year, month):
#     start_date = date(year, month, 1)
#     last_day = calendar.monthrange(year, month)[1]  # 月の最終日
#     end_date = date(year, month, last_day)
#     return start_date, end_date

# # 指定した月のすべてのデータを取得する
# def fetch_events_for_month(connection, year, month):
#     start_date, end_date = get_month_range(year, month)
#     query = select(Calendar).where(Calendar.c.day.between(start_date, end_date))
#     result = connection.execute(query)
#     return result.fetchall()



# 現在の年月のカレンダーを作成
@Calen.route('/')
def index():
    # 現在の年と月を取得
    now = datetime.now()
    year = now.year
    month = now.month

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # date_string = f"{year}-{month}"

    return render_template('calendar/calendar.html',
                           year=year, month=month, month_days=month_days)


# 次の月のカレンダーを作成
@Calen.route('/next<int:year>/<int:month>')
def nextindex(year, month):

    # 12月の次を1月にして、年に1を足す
    if month == 12:
        year = year + 1
        month = 1
    else:
        year = year
        month = month + 1

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month,
                           month_days=month_days)


# 先月のカレンダーを作成
@Calen.route('/before/<int:year>/<int:month>')
def beforeindex(year, month):
    # 12月の次を1月にして、年に1を引く
    if month == 1:
        year = year - 1
        month = 12
    else:
        year = year
        month = month - 1

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month,
                           month_days=month_days)


# カレンダー登録のエンドポイント
@Calen.route('/register', methods=["GET", "POST"])
def setEvent():
    # カレンダーフォームをインスタンス化
    form = CalendarregistForm()

    if form.validate_on_submit():
        calen = Calendar(
            event_title=form.title.data,
            content=form.text.data,
            day=form.date.data,
            local_id="abc"
        )

        db.session.add(calen)
        db.session.commit()
        return redirect(url_for("calendar.index"))

    return render_template("calendar/register.html", form=form)


# カレンダー編集のエンドポイント
@Calen.route("/event_edit/<calendar_id>", methods=["GET", "POST"])
def edit_event(calendar_id):
    form = CalendarregistForm()
    event = Calendar.query.get_or_404(calendar_id)
    if form.validate_on_submit():
        event.event_title = form.title.data,
        event.content = form.text.data,
        event.day = form.date.data,
        event.local_id = "abc"

        db.session.commit()
        return redirect(url_for("calendar.index"))

    # フォームの初期値に投稿データをセット
    form.title.data = event.event_title
    form.text.data = event.content
    form.date.data = event.day

    return render_template("calendar/event_edit.html", form=form, event=event)


# カレンダーイベント削除のエンドポイント
@Calen.route('/<int:calendar_id>/delete', methods=['POST'])
def delete(calendar_id):
    # 削除処理
    calen = Calendar.query.get(calendar_id)
    if calen:
        db.session.delete(calen)
        db.session.commit()
    flash('イベントを削除しました')
    return redirect(url_for('calendar.index'))  # 削除が完了するとtopページに遷移


# 選択された日のイベント一覧
@Calen.route('/events/<date>')
def events(date):
    from datetime import datetime
    selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    events = Calendar.query.filter_by(day=selected_date).all()
    return render_template('calendar/event_list.html', date=selected_date,
                           events=events)


# 選択された年月のカレンダーを表示
@Calen.route('/select/<int:year>/<int:month>')
def selectindex(year, month):
    year = year
    month = month

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month,
                           month_days=month_days)


# カレンダー詳細のエンドポイント
@Calen.route("/event_detail/<calendar_id>", methods=["GET"])
def event_detail(calendar_id):
    event = Calendar.query.get_or_404(calendar_id)
    date = event.day

    return render_template("calendar/event_detail.html",
                           event=event, date=date)
