from flask import Flask,Blueprint, request, jsonify, render_template
from flask_login import current_user
from minimalapp.tags.models import Local
from app import db
from minimalapp.ai.forms import AiForm
import json

from PIL import Image
import torch
from torchvision import transforms, models
from torchvision.models import efficientnet_b7, EfficientNet_B7_Weights
from transformers import pipeline,AutoTokenizer, AutoModelForCausalLM


# Bulueprintでaiアプリを生成する
ai = Blueprint(
    "ai",
    __name__,
    template_folder="templates",
    static_folder="../static"
)

# モデルとトークナイザーの読み込み
tokenizer = AutoTokenizer.from_pretrained("rinna/japanese-gpt-1b", use_fast=False)
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")

if torch.cuda.is_available():
    model = model.to("cuda")

# 画像認識用のモデル
image_model = efficientnet_b7(weights=EfficientNet_B7_Weights.DEFAULT)
image_model.eval()

# 画像処理のトランスフォーム
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])



@ai.route("/ai_question")
def ai_question():
    form = AiForm()
    return render_template("ai/ai_question.html", form=form)

@ai.route("/ai_answer",methods=["POST"])
def ai_answer():
    form = AiForm()

    # 画像のアップロード
    file = form.image.data
    image = Image.open(file).convert("RGB")

    # 画像認識処理
    input_tensor = preprocess(image).unsqueeze(0)
    
    with torch.no_grad():
        outputs = image_model(input_tensor)
    _, predicted = outputs.max(1)

    predicted_class_id = predicted.item()  
    # クラスID（予測されたクラスID）
    # print(f"予測されたクラスID: {predicted_class_id}")

    # JSONファイルの読み込み
    with open('imagenet_class_index.json', 'r', encoding='utf-8') as f:
        class_idx = json.load(f)
    
    # クラスIDに基づいてクラス名を取得
    class_name = class_idx.get(str(predicted_class_id), "不明なクラス")


    # JSONファイルの読み込み
    with open('imagenet_class_index_ja.json', 'r', encoding='utf-8') as f:
        class_idx_ja = json.load(f)
    
    # クラスIDに基づいて日本語名を取得
    class_name_ja = "不明なクラス"  # デフォルトのクラス名

    for entry in class_idx_ja:
        if entry['num'] == class_name[0]:  # 予測されたクラスIDで検索
            class_name_ja = entry['ja']  # 日本語名を取得
            break  # 見つかったらループを抜ける
        

    # 画像認識情報を基に質問を生成
    prompt = f"{class_name_ja}について簡潔に説明してください。"

    # 入力トークンのエンコード
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    input_ids = input_ids.to(model.device)


    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_length=200,
            min_length=100,
            do_sample=True,
            top_k=5,
            top_p=1.0,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            bad_words_ids=[[tokenizer.unk_token_id]]
        )

    output = tokenizer.decode(output_ids.tolist()[0], skip_special_tokens=True)
    # print(output)

    # 出力から「{class_name_ja}について簡潔に説明してください。」部分を削除
    explanation = output.replace(f"{class_name_ja}について簡潔に説明してください。", "").strip()
    return render_template("ai/ai_answer.html", class_name=class_name_ja,explanation=explanation)


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