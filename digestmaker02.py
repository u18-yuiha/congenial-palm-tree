
import subprocess
import os


def mk_starts_ends(movie):
    
    output = subprocess.run(["ffmpeg","-vn" ,"-i", movie, "-af", "silencedetect=noise=-13dB:d=0.5", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #"-f", "null", "-"これで、ファイルを出力しないようにしている。ffmprobeでよくない？
    # "-af", "silencedetect=noise=-33dB:d=0.6"オーディオの設定。ノイズのデシベルと、秒数の指定。
    #print(output)
    s = str(output)
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
   
    
    
    print(time_list,12345)
    starts_ends = list(zip(*[iter(time_list)]*2))
    print(starts_ends)
    return starts_ends

#mk_starts_ends(path)

#path = '入力する動画のパス'
#output ='出力する動画のパス'
path = 'C:\\Users\AraiAkihiko\Videos\Exp\ダイジェストメーカ―サンプル.mp4'
output ='C:\\Users\AraiAkihiko\Videos\Exp\サブプロセス実験02.mp4'
chunks = mk_starts_ends(path)

#５、③で得られた無音部分をもとに、音声のある場所を検出、分割。
merge_list = [[chunks[i][1],chunks[i + 1][0]] for i in range(len(chunks)) if i <= len(chunks) - 2]


print(merge_list)

#6,⑤で得られた音声のある部分の情報をもとに、動画の分割
#moviepyをインポート
from moviepy.editor import *

#moviepyに動画を読み込ませる
video = VideoFileClip(path)
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
result.write_videofile(output)