#ffmpeg,ffmpeg-python,pydub,moviepyをインストールしてから使ってください。

#1 動画読み込み,音声抽出(mp3),
import ffmpeg
import sys

#入力用のファイルのパス
path = rf"無音カットしたい動画のファイルのパス"
#途中出力される無音部分検出用の音声ファイル
audio_path = rf'途中出力される無音部分検出用の音声ファイルのパス（後で削除することを推奨）'
"""
必ず出力用の端子は.mp3にすること!!!
"""
#出力用のファイルのパス
output = rf"出力用のファイルのパス"


(
        ffmpeg
        .input(path)
        .output(audio_path, acodec = "mp3", crf=30, preset='fast',vcodec = "-vn")
        .run()
    )

#3音声を読み込んで、一定の音量以下の部分を計測(成功)
from pydub import AudioSegment
from pydub.silence import *

sound = AudioSegment.from_file(audio_path, format="mp3")
chunks = detect_silence(
    sound,

    # 500ms以上の無音がある
    min_silence_len=500,

    # -15dBFS以下で無音とみなす
    silence_thresh=-25, 

    
    
    seek_step = 1
)

#print(chunks)
#4音声の秒数を計測
duration = sound.duration_seconds


#５、③で得られた無音部分をもとに、音声のある場所を検出、分割。
merge_list = [[chunks[i][1],chunks[i + 1][0]] for i in range(len(chunks)) if i <= len(chunks) - 2]

#音声の始まりが無音ではなかった場合,最初の部分をつける
if chunks[0][0] != 0:
    merge_list.insert(0,[0,chunks[0][1]])
#音声の終わりが無音ではなかった場合、最後の部分をつける
duration = 66.64126984126985
if chunks[-1][1] != int(duration * 1000):
    merge_list.insert(-1,[chunks[-1][1],int(duration * 1000)])

print(merge_list)

#動画の分割
#moviepyをインポート
from moviepy.editor import *
video = VideoFileClip(path)

clips = {}
count = 0
for i in range(len(merge_list)):
    clips[count] = video.subclip(merge_list[i][0]/1000,merge_list[i][1]/1000)
    count += 1

videos = [clips[i] for i in range(count)]
result = concatenate(videos)
result.write_videofile(output)
