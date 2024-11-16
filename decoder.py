import json

# 入力ファイルと出力ファイルのパス
input_file = "kyok.json"  # デコードするJSONファイル
output_file = "output.json"  # デコード後のJSONを保存するファイル

# JSONファイルを開いて読み込む
with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)  # JSONデコード（Unicodeエスケープが解消される）

# デコード後のデータを新しいファイルに書き出す
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)  # `ensure_ascii=False`でエスケープを防ぐ

print("デコード済みのJSONを保存しました:", output_file)
