import subprocess
import os
#import moviepy
from moviepy.editor import *
import sys
def mk_starts_ends(movie):
    
    output = subprocess.run(["ffmpeg","-vn" ,"-i", movie, "-af", "silencedetect=noise=-13dB:d=0.5", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    #"-vn"処理速度向上のため、これで動画部分を無視させている。
    # "-af", "silencedetect=noise=-33dB:d=0.6"オーディオの設定。ノイズのデシベルと、秒数の指定。
    #print(output)
    
    s = str(output)
    #改行のマークごとに分割
    lines = s.split('\\n')
    #print("\n",lines,1234567890)
    time_list =[]
    #######################################################################
    for line in lines:
        if "silencedetect" in line:
            words = line.split(" ")
            #print("\n",words,11111)
            for i in range(len(words)):
                if "silence_start" in words[i]:
                    #words[i + 1].lstrip("\\r")
                    #print("\n",12345,words[i + 1])
                    time_list.append(float(words[i+1].replace('\\r','')))
                if "silence_end" in words[i]:
                    #words[i + 1].lstrip("")
                    time_list.append(float(words[i+1].replace('\\r','')))
    #####################################################################
   
    
    
    #print(time_list,12345)
    starts_ends = list(zip(*[iter(time_list)]*2))
    print(starts_ends)
    return starts_ends



def cut_videos(path,output,chunks):
    
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

    if chunks[-1][1] != int(duration * 1000):
        merge_list.insert(-1,[chunks[-1][1],int(duration)])

    #clipsという空のディクトに、音声のある部分を入れていく。
    clips = {}

    #音声のある部分を入れた数をカウントする
    count = 0

    for i in range(len(merge_list)):
        clips[count] = video.subclip(merge_list[i][0],merge_list[i][1])
        count += 1

    #listがたのから集合にclipsを入れていく
    videos = [clips[i] for i in range(count)]
    #concatenateで、それらを合体させていく
    result = concatenate(videos)
    #.write_videofileで合体させたものを動画として出力。
    result.write_videofile(output,fps = 20)



#使用例、rfをつけているのはWindowsの使用上の問題（￥）
if __name__ == "__main__":
    path = rf"入力する動画のパス"
    chunks = mk_starts_ends(path)

    output = rf"出力する動画のパス"

    cut_videos(path,output,chunks)