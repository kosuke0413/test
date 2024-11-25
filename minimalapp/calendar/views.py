from flask import Blueprint,render_template,redirect,url_for
from datetime import datetime
import calendar
from minimalapp.calendar.forms import CalendarregistForm
from minimalapp.calendar.models import Calendar
from app import db

#Blueprintでcalendarアプリを生成する
Calen = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

#現在の年月のカレンダーを作成
@Calen.route('/')
def index():
    # 現在の年と月を取得
    now = datetime.now()
    year = now.year
    month = now.month

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month, month_days=month_days)


#次の月のカレンダーを作成
@Calen.route('/next<int:year>/<int:month>')
def nextindex(year, month):
    
    #12月の次を1月にして、年に1を足す
    if month == 12:
        year = year + 1
        month = 1
    else:
        year = year
        month = month + 1

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month, month_days=month_days)

#先月のカレンダーを作成
@Calen.route('/before/<int:year>/<int:month>')
def beforeindex(year, month):
    #12月の次を1月にして、年に1を引く
    if month == 1:
        year = year - 1
        month = 12
    else:
        year = year
        month = month - 1

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month, month_days=month_days)


#カレンダー登録のエンドポイント
@Calen.route('/register', methods=["GET", "POST"])
def setEvent():
    #カレンダーフォームをインスタンス化
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
        return redirect(url_for("calendar/calendar"))

    return render_template("calendar/register.html", form=form)

# @Calen.route("/event_edit/<calendar_id>", methods=["GET", "POST"])
# def edit_event(calendar_id):
#     form = CalendarregistForm():

#     event = Calendar.query.filter_by(id=calendar_id).first()

#     if form.validate_on_submit():
#         calen = Calendar(
#             event.event_title=form.title.data,
#             content=form.text.data,
#             day=form.date.data,
#             local_id="abc"
#         )

#         db.session.add(calen)
#         db.session.commit()
#         return "登録完了"

#     return render_template("calendar/calendar.html", form=form)



#選択された日のイベント一覧
# @app.route('/events/<date>')
# def events(date):
#     from datetime import datetime
#     selected_date = datetime.strptime(date, "%Y-%m-%d").date()
#     events = Event.query.filter_by(date=selected_date).all()
#     return render_template('events.html', date=selected_date, events=events)
