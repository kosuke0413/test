from flask import Flask,Blueprint, request, jsonify, render_template
from flask_login import current_user
from minimalapp.tags.models import Local
from app import db
from minimalapp.ai.forms import AiForm
import json

from PIL import Image
import torch
from torchvision import transforms, models
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


# 画像認識用のモデル（ResNet50を使用）
image_model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
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

    predicted_class_id = predicted.item()  # クラスID（予測されたクラスID）
    # print(f"予測されたクラスID: {predicted_class_id}")

    # JSONファイルの読み込み
    with open('imagenet_class_index.json', 'r', encoding='utf-8') as f:
        class_idx = json.load(f)
    
    # クラスIDに基づいてクラス名を取得
    class_name = class_idx.get(str(predicted_class_id), "不明なクラス")
    # print(f"予測されたクラス名: {class_name}")
    # print("ID名" + class_name[0])

    # JSONファイルの読み込み
    with open('imagenet_class_index_ja.json', 'r', encoding='utf-8') as f:
        class_idx_ja = json.load(f)
    
    # クラスIDに基づいて日本語名を取得
    class_name_ja = "不明なクラス"  # デフォルトのクラス名

    for entry in class_idx_ja:
        if entry['num'] == class_name[0]:  # 予測されたクラスIDで検索
            class_name_ja = entry['ja']  # 日本語名を取得
            break  # 見つかったらループを抜ける

    # print(f"日本語名:{class_name_ja}")
    # text = form.text.data + "は、"

    text = class_name_ja + "は、"
    
    token_ids = tokenizer.encode(text, add_special_tokens=False, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            token_ids.to(model.device),
            max_length=100,
            min_length=100,
            do_sample=True,
            top_k=5,
            top_p=1.0,
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