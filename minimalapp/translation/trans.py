import argostranslate.package
import argostranslate.translate

from_code = "en"
to_code = "ja"

# 翻訳パッケージのインデックスをアップデート
argostranslate.package.update_package_index()
# 有効なパッケージの取得
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
# パッケージのインストール
argostranslate.package.install_from_path(package_to_install.download())

translatedText = argostranslate.translate.translate("Hello World", from_code, to_code)
print(translatedText)
# 'ハローワールド'