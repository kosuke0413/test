from flask import Blueprint,render_template
from datetime import datetime
import calendar

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