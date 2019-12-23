import subprocess
import os
from moviepy.editor import *
import sys
def mk_starts_ends(movie,threshold,silence_section):
    
    output = subprocess.run(["ffmpeg","-vn" ,"-i", movie, "-af", f"silencedetect=noise={threshold}dB:d={silence_section}", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    
    
    s = str(output)
    lines = s.split('\\n')
    
    time_list =[]
    
    for line in lines:
        if "silencedetect" in line:
            words = line.split(" ")
            
            for i in range(len(words)):
                if "silence_start" in words[i]:
                    
                    time_list.append(float(words[i+1].replace('\\r','')))
                if "silence_end" in words[i]:
                    
                    time_list.append(float(words[i+1].replace('\\r','')))
        #inputが空だった場合、
        if "No such file or directory" in line:
            print(">>動画を読み込めませんでした。パスが間違っている可能性があります。")
            print(">>Could not load video. The path may be wrong.")
        #inputが動画ではなかった場合
        if  "does not contain any stream"in line:
            print(">>動画を読み込めませんでした。動画以外を入力している可能性があります。")
            print(">>Could not load video. You may have entered something other than a video.")
            
    
    starts_ends = list(zip(*[iter(time_list)]*2))

    return starts_ends



def cut_videos(path,output,chunks,FPS):
    
    #moviepyに動画を読み込ませる
    video = VideoFileClip(path)
    #動画の長さを図る
    duration = video.duration

    #５、③で得られた無音部分をもとに、音声のある場所を検出、分割。
    merge_list = [[chunks[i][1],chunks[i + 1][0]] for i in range(len(chunks)) if i <= len(chunks) - 2]
    #音声の始まりが無音ではなかった場合,最初の部分をつける
    if chunks[0][0] != 0:
        merge_list.insert(0,[0,chunks[0][1]])
    #音声の終わりが無音ではなかった場合、最後の部分をつける

    if chunks[-1][1] >= int(duration * 1000):
        merge_list.insert(-1,[chunks[-1][1],int(duration)])

    clips = {}
    count = 0

    for i in range(len(merge_list)):
        clips[count] = video.subclip(merge_list[i][0],merge_list[i][1])
        count += 1

    
    videos = [clips[i] for i in range(count)]

    result = concatenate(videos)
    #fpsは高いほど画質が良くなる。（15～60の間が推奨）
    result.write_videofile(output,fps = FPS)

if __name__ == "__main__":
    #パスに「。」や「、」空白などが含まれていると、エラーを起こす可能性がある。
    path = rf"入力する動画のパス"
    #閾値。この音量以下の部分を無音とみなす。（－10～－40辺りを推奨）
    threshold = -15
    #無音の部分がsilence_section秒あったらそれを無音区間とする（0.4～2.0辺りを推奨）
    silence_section = 0.6
    try:
        chunks = mk_starts_ends(path,threshold,silence_section)
    except OSError:
        print("外部のアプリケーションとの連携が取れていない可能性があります\nパソコンを再起動してみてください。")
    else:
        chunks = mk_starts_ends(path,threshold,silence_section)
    print(chunks)

    if chunks == []:
            print(">>無音区間の検出ができませんでした。　処理を終了します。")
            print(">>No silent section could be detected.　Terminates processing.")
            pass

    else:
        try:
            output = rf"出力する動画のパス"
            #FPSは高いほど画質が良くなる。（15～60の間が推奨）
            FPS = 10
            cut_videos(path,output,chunks,FPS)
        except OSError:
            print("出力用のパスの端子（.mp4など）が間違っているか、")
            print("フォルダやファイル名に「。」や「、」空白などが含まれている、もしくは、")
            print("出力用のファイルが既に存在している可能性があります。")
        else:
            cut_videos(path,output,chunks,FPS)


