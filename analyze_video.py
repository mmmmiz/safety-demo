import google.genai as genai
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 動画をアップロード
print("アップロード中・・・")

video_file = client.files.upload(
    file = "sample.mp4",
)
print(f"アップロード完了！ファイル名：{video_file.name}")

# Geminiがファイルを処理し終わるまで待つ
print("Geminiが動画を処理中・・・")

assert video_file.name is not None
while video_file.state is not None and video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)
    print(f"状態：{video_file.state.name}")
if video_file.state.name !="ACTIVE":
    raise Exception(f"動画の処理に失敗しました。状態：{video_file.state.name}")
print("動画の処理完了！解析を開始します・・・")

# プロンプトを作る
prompt = """
あなたは工場の安全管理AIです。
この動画を見て、作業員の安全状態を確認してください。

以下のJSON形式【のみ】で回答してください。前置きや説明文は不要です。

{
  "helmet": {
    "status": "着用済み" または "未着用" または "確認不可",
    "detail": "詳細の説明"
  },
  "danger_zone": {
    "status": "問題なし" または "接近あり" または "侵入あり",
    "detail": "詳細の説明"
  },
  "abnormal_posture": {
    "status": "問題なし" または "要確認" または "転倒疑い",
    "detail": "詳細の説明"
  },
  "overall": {
    "status": "安全" または "要注意" または "危険",
    "reason": "総合評価の理由"
  }
}
"""


