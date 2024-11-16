import os
from googleapiclient.discovery import build
import yt_dlp
import pydub
from pydub import AudioSegment
from pytube import YouTube
import json
import librosa
from moviepy.editor import AudioFileClip
from zigoe import path_async
import multiprocessing
import asyncio
# YouTube APIキー
API_KEY = 'AIzaSyCA1UwHcgu0TApJqUsMxP1h312rGwtZ-hk'


# 1. YouTube APIを使って音楽動画のIDを取得（音楽カテゴリに限定）
def get_video_id(song_name):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    request = youtube.search().list(
        q=song_name,  # 検索キーワード
        part='snippet',
        type='video',
        regionCode='JP',  # 日本地域に限定
        relevanceLanguage='ja',  # 日本語での関連性を優先
        videoCategoryId='10',  # 音楽カテゴリに限定
        maxResults=50,
    )
    response = request.execute()
    
    # 音楽関連の動画が見つかったか確認
    if response['items']:
        print(f"get len({len(response['items'])})")
        return[(item['id']['videoId'],item['snippet']['title']) for item in response['items']]
    else:
        print("No music videos found for the given song name.")
        return None

# 2. 動画の音声をダウンロード
async def download_audio(video_id,path="output"):
    print(f'https://www.youtube.com/watch?v={video_id}')
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    # yt-dlpの設定
    ydl_opts = {
        'format': 'bestaudio/best',  # 音声のみをダウンロード
        'outtmpl': f'{path}.%(ext)s',   # 出力ファイル名
    }

    # 音声をダウンロード
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    print(f"Audio downloaded as '{path}.mp3'")



# 3. 音声ファイルをWAV形式に変換
async def convert_to_wav(path="output"):
    try:
        audio_clip = AudioFileClip(f"{path}.mp3")
        audio_clip.write_audiofile(f"{path}.wav", codec='pcm_s16le')
        os.remove(f"{path}.mp3")
    except:
        try:
            audio_clip = AudioFileClip(f"{path}.webm")
            audio_clip.write_audiofile(f"{path}.wav", codec='pcm_s16le')
            os.remove(f"{path}.webm")
        except Exception as e:
            print(e)
            print("第っ失敗")
            exit()
    print("Converted to '{path}.wav'")

async def wrapper(video_id,title):
    await download_audio(video_id,path=f"audio{video_id}")
    await convert_to_wav(path=f"audio{video_id}")
    print("I/o終了",title,video_id)
def run_async_task(item):
    loop = asyncio.get_event_loop()
    data=loop.run_until_complete(path_async(item[0]))
    print("音声処理終了",*item)
    with open("output.txt","a",encoding="utf-8") as f:
        f.write(f'name:{item[1]},min:{data["min"]},max:{data["max"]}\n')
    return {"name":item[1],"min":data["min"],"max":data["max"]}
# メイン処理
async def main():
    global json_data
    # 楽曲を検索して動画IDを取得
    video_list = get_video_id("")
    video_list=[(id,title) for id,title in video_list if not id in json_data ]
    print(len(video_list),"こだな")
    if video_list:
        tasks = [wrapper(video_id,title) for video_id, title in video_list]
        await asyncio.gather(*tasks)
    with multiprocessing.Pool() as pool:
        pool.map(run_async_task,[(os.path.abspath(f"audio{video_id}.wav"),title) for video_id, title in video_list])

if __name__ == "__main__":
    jsonpath="kyok.json"
    with open(jsonpath, 'r',encoding="utf-8") as file:
        json_data = json.load(file)
    asyncio.run(main())
    with open(jsonpath, 'w',encoding="utf-8") as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)  # indent=4で見やすいフォーマットに
        print("完了")