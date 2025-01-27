from flask import Blueprint, render_template, redirect, url_for, flash
from datetime import datetime, date
import calendar
from minimalapp.calendar.forms import CalendarregistForm
from minimalapp.calendar.models import Calendar
from app import db
from collections import defaultdict
from flask_login import login_required, current_user
from minimalapp.tags.models import Local

# Blueprintでcalendarアプリを生成する
Calen = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
    static_folder="../static"
)


# 現在の年月のカレンダーを作成
@Calen.route('/')
@login_required
def index():
    # 現在の年と月を取得
    now = datetime.now()
    year = now.year
    month = now.month

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # 月の開始日と終了日を取得
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # 該当月のすべてのイベントを取得
    events = Calendar.query.filter(
        Calendar.day.between(start_date, end_date),  # 範囲フィルタ
        Calendar.local_id == current_user.local_id  # ローカルIDフィルタ
        ).all()
    event_days = defaultdict(list)
    for event in events:
        event_days[event.day.day].append(event)  # 日付のみに絞って保存

    return render_template(
        'calendar/calendar.html',
        year=year, month=month, month_days=month_days, event_days=event_days,
        events=events,
    )


# 次の月のカレンダーを作成
@Calen.route('/next<int:year>/<int:month>')
def nextindex(year, month):
    # 現在、100年後の年、100年前の年を計算
    now = datetime.now()
    max_year = now.year + 100
    min_year = now.year - 100

    # 次の月が制限を超えたら現在の月に戻す
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

    # 表示年月が前後に100年を超えた場合は、現在の年月に戻る
    if year > max_year or (year == max_year and month > now.month) or year < min_year or (year == min_year and month < now.month):
        # flash("これ以上進めません。")
        return redirect(url_for('calendar.index'))

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # 月の開始日と終了日を取得
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # 該当月のすべてのイベントを取得
    events = Calendar.query.filter(
        Calendar.day.between(start_date, end_date),  # 範囲フィルタ
        Calendar.local_id == current_user.local_id  # ローカルIDフィルタ
    ).all()
    event_days = defaultdict(list)
    for event in events:
        event_days[event.day.day].append(event)  # 日付のみに絞って保存

    return render_template('calendar/calendar.html', year=year, month=month,
                           month_days=month_days, event_days=event_days,
                           events=events)


# 先月のカレンダーを作成
@Calen.route('/before/<int:year>/<int:month>')
def beforeindex(year, month):
    # 現在、100年後の年、100年前の年を計算
    now = datetime.now()
    max_year = now.year + 100
    min_year = now.year - 100

    # 前の月が制限を下回ったら現在の月に戻す
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

    if year > max_year or (year == max_year and month > now.month) or year < min_year or (year == min_year and month < now.month):
        # flash("これ以上戻れません。")
        return redirect(url_for('calendar.index'))

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # 月の開始日と終了日を取得
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # 該当月のすべてのイベントを取得
    events = Calendar.query.filter(
        Calendar.day.between(start_date, end_date),  # 範囲フィルタ
        Calendar.local_id == current_user.local_id  # ローカルIDフィルタ
    ).all()
    event_days = defaultdict(list)
    for event in events:
        event_days[event.day.day].append(event)  # 日付のみに絞って保存

    return render_template('calendar/calendar.html', year=year, month=month,
                           month_days=month_days, event_days=event_days,
                           events=events)


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
            local_id=current_user.local_id
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
    events = Calendar.query.filter(Calendar.day == selected_date,
                                   Calendar.local_id == current_user.local_id
                                   ).all()
    return render_template('calendar/event_list.html', date=selected_date,
                           events=events)


# 選択された年月のカレンダーを表示
@Calen.route('/select/<int:year>/<int:month>')
def selectindex(year, month):
    year = year
    month = month

        # 現在、100年後の年、100年前の年を計算
    now = datetime.now()
    max_year = now.year + 100
    min_year = now.year - 100

    # 前の月が制限を下回ったら現在の月に戻す
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

    # 上限の100年を超えないように指定
    if year > max_year or (year == max_year and month > now.month) or year < min_year or (year == min_year and month < now.month):
        return redirect(url_for('calendar.index'))
    

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    # 月の開始日と終了日を取得
    start_date = date(year, month, 1)
    last_day = calendar.monthrange(year, month)[1]
    end_date = date(year, month, last_day)

    # 該当月のすべてのイベントを取得
    events = Calendar.query.filter(
        Calendar.day.between(start_date, end_date),  # 範囲フィルタ
        Calendar.local_id == current_user.local_id  # ローカルIDフィルタ
        ).all()
    event_days = defaultdict(list)
    for event in events:
        event_days[event.day.day].append(event)  # 日付のみに絞って保存

    return render_template('calendar/calendar.html', year=year, month=month,
                           month_days=month_days, event_days=event_days,
                           events=events)


# カレンダー詳細のエンドポイント
@Calen.route("/event_detail/<calendar_id>", methods=["GET"])
def event_detail(calendar_id):
    event = Calendar.query.get_or_404(calendar_id)
    date = event.day

    if current_user.manager_flag is True:
        return redirect(url_for("calendar.edit_event",
                                calendar_id=calendar_id))

    return render_template("calendar/event_detail.html",
                           event=event, date=date)


@Calen.context_processor
def inject_local():
    # 未ログイン時は地域名を未定義にする
    if current_user.is_anonymous:
        return {"local": {"local_name": "未定義"}}

    local = Local.query.get(current_user.local_id)
    print(current_user.local_id)
    if local:
        return {
            "local": {"local_name": local.local_name}
        }

    else:
        return {"local": {"local_name": "未定義"}}
    
    
