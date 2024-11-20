from flask import Blueprint,render_template
from datetime import datetime
import calendar
from minimalapp.calendar.forms import CalendarregistForm
from minimalapp.calendar.models import Calendar
from app import db

#Blueprintでcalendarアプリを生成する
Calendar = Blueprint(
    "calendar",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

@Calendar.route('/')
def index():
    # 現在の年と月を取得
    now = datetime.now()
    year = now.year
    month = now.month

    # カレンダーを作成
    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year, month)

    return render_template('calendar/calendar.html', year=year, month=month, month_days=month_days)

#カレンダー登録のエンドポイント
@Calendar.route('/register', methods=["GET","POST"])
def setEvent():
    #カレンダーフォームをインスタンス化
    form = CalendarregistForm()

    if form.validate_on_submit():
        calen = Calendar(
            event_title = form.title.data,
            content = form.text.data,
            day = form.date.data
        )

    db.session.add(calen)
    db.session.commit()
    return "登録完了"

return render_template("calendar/register.html")

