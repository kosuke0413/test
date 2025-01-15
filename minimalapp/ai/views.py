from flask import Flask,Blueprint, request, jsonify, render_template
from flask_login import current_user
from minimalapp.tags.models import Local
from app import db
from minimalapp.ai.forms import AiForm
import json

import torch
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM


# Bulueprintでaiアプリを生成する
ai = Blueprint(
    "ai",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt-1b", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")

if torch.cuda.is_available():
    model = model.to("cuda")

@ai.route("/ai_question")
def ai_question():
    form = AiForm()
    return render_template("ai/ai_question.html", form=form)

@ai.route("/ai_answer",methods=["POST"])
def ai_answer():
    form = AiForm()
    text = form.text.data + "について説明します"
    
    token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            max_length=100,
            min_length=100,
            do_sample=True,
            top_k=500,
            top_p=0.95,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_words_ids=[[tokenizer.unk_token_id]]
        )

    output = tokenizer.decode(output_ids.tolist()[0])
    print(output)
    return output


@ai.context_processor
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