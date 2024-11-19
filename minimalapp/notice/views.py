from flask import Blueprint,render_template

#Bulueprintでnoticeアプリを生成する
notice = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

notice_reply = Blueprint(
    "notice_reply",
    __name__,
    template_folder="templates",
    static_folder="../static"
)