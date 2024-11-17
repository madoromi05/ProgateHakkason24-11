import json
from googleapiclient.discovery import build
import random
import string
API_KEY = 'AIzaSyCA1UwHcgu0TApJqUsMxP1h312rGwtZ-hk'
youtube = build('youtube', 'v3', developerKey=API_KEY)
def get_video_id_by_title(title):
    # API で検索を実行
    request = youtube.search().list(
        part='snippet',
        q=title,       # 検索クエリ (タイトル)
        type='video',  # 動画のみを検索
        maxResults=1   # 最初の1件のみ取得
    )
    response = request.execute()

    # レスポンスから動画 ID を取得
    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        return video_id
    else:
        return None
# ファイルを読み込む
with open('output.txt', 'r', encoding='utf-8') as file:
    lines = [line for line in file]
    print(len(lines),"ko")
def generate_random_string(length=16):
    # 英数字を選択肢とする
    characters = string.ascii_letters + string.digits
    # 指定された長さのランダム文字列を生成
    return ''.join(random.choice(characters) for _ in range(length))
# 既存のJSONデータを読み込む
try:
    with open('kyok.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    # output.jsonが存在しない場合、新しい辞書を作成
    json_data = {}

for line in lines:

    nameindex=line.find("name:")
    minindex=line.find(",min:")
    maxindex=line.find(",max:")
    name=line[nameindex:minindex]
    min=line[minindex:maxindex]
    max=line[maxindex:]
    id=get_video_id_by_title(name)
    if id==None:
        id=generate_random_string()
    json_data[id]={
        "name":name[name.find(":")+1:],
        "min":min[min.find(":")+1:],
        "max":max[max.find(":")+1:]
    }

# 更新されたJSONデータを保存
with open('kyok.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print("JSONファイルが更新されました！")
