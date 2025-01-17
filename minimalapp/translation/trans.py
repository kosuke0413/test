from googletrans import Translator

# Translatorのインスタンスを作成
translator = Translator()

# ユーザーに入力を促す(日本語)
catchphrase = input("翻訳したいフレーズを入力してください: ")

# 翻訳を実行(英語)
translated = translator.translate(catchphrase)

# 翻訳結果を表示(英語)
print(f"翻訳結果: {translated.text}")
