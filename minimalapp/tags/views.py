from flask import Blueprint

# Bulueprintでnoticeアプリを生成する
tags = Blueprint(
    "tags",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

# @tags.route("/")
# def index():
#     return "Hello Tags"
