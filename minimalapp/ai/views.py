from flask import Flask,Blueprint, request, jsonify, render_template
from minimalapp.ai.forms import AiForm
import json

from PIL import Image
import torch
from torchvision import transforms,models
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

@ai.route("/")
def index():
    text = "cssとは、"
    
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