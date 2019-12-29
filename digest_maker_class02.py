import subprocess
import os
from moviepy.editor import *
import sys
import os.path

class DigestMaker:
    
    def __init__(self,path,output = None,threshold = -15,silence_section = 0.5):
        try:
            self.path = path
            self.output = output
            self.threshold = threshold
            self.silence_section = silence_section
            self.video = VideoFileClip(self.path)
        except OSError:
            print("外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
            
    
    def get_info(self):
    
        info = subprocess.run(["ffmpeg","-vn" ,"-i", self.path, "-af", f"silencedetect=noise={self.threshold}dB:d={self.silence_section}", "-f", "null", "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        
        # "-af", "silencedetect=noise=-33dB:d=0.6"オーディオの設定。ノイズのデシベルと、秒数の指定。
        
        info = str(info)
        return info
    def silence_detect(self,info):
        self.info = info
        lines = info.split('\\n')
        
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
                return False
            
            if  "does not contain any stream"in line:
                print(">>動画を読み込めませんでした。動画以外を入力している可能性があります。")
                print(">>Could not load video. You may have entered something other than a video.")
                return False
                
        starts_ends = list(zip(*[iter(time_list)]*2))
        #print(starts_ends)
        return starts_ends



    def using_parts(self,starts_ends):
        
        
        #動画の長さを図る
        duration = self.video.duration

        #５、③で得られた無音部分をもとに、音声のある場所を検出、分割。
        self.merge_list = [[starts_ends[i][1],starts_ends[i + 1][0]] for i in range(len(starts_ends)) if i <= len(starts_ends) - 2]
        #音声の始まりが無音ではなかった場合,最初の部分をつける
        if starts_ends[0][0] != 0:
            self.merge_list.insert(0,[0,starts_ends[0][1]])
        #音声の終わりが無音ではなかった場合、最後の部分をつける

        if starts_ends[-1][1] >= int(duration * 1000):
            self.merge_list.insert(-1,[starts_ends[-1][1],int(duration)])
        return self

    def concatenate_videos(self):      
        clips = {}      
        count = 0

        for i in range(len(self.merge_list)):
            clips[count] = self.video.subclip(self.merge_list[i][0],self.merge_list[i][1])
            count += 1
        
        #listがたのから集合にclipsを入れていく
        videos = [clips[i] for i in range(count)]
        #concatenateで、それらを合体させていく
        result = concatenate(videos)
        #.write_videofileで合体させたものを動画として出力。
        result.write_videofile(self.output,fps = 20,preset = "superfast")
        

def change(path):
    path =  path.replace("\\","/")
    return path
    
def dir_for_check(path):
    lines = path.split("/")
    rm_file = "/" + lines[-1]
    check_dir = path.replace(rm_file,"")
    return check_dir
        
    
#if name == main():
if True:
    
    path = rf'入力する動画のパス'
    
    output =rf'出力する動画のパス'
    
    path = change(path)
    print(path)
    #入力する動画のパスが存在することの確認
    judge_input = os.path.exists(path)
    output = change(output)
    #出力する動画のフォルダーのパスが存在することの確認
    judge_output = dir_for_check(output)
    print(judge_output)
    #出力する動画のファイルのパスが存在しないことの確認
    judge_output = os.path.exists(judge_output)
    judge_not_exist_output = os.path.exists(output)
    
    if judge_input == judge_output == False:
        print("入力用のパスと出力用のパスのどちらも間違っている可能性があります。")
        pass
    elif judge_input == True and judge_output == False:
        print("出力用のフォルダのパスが間違っている可能性があります。")
        pass
    elif judge_input == False and judge_output == True:
        print("入力用のパスが間違っている可能性があります。")
        pass
    elif  judge_input == judge_output == judge_not_exist_output == True:
        print("出力用のファイルのパスが既に存在しています。")
        pass
    else:
        print("読み込みを開始します。")
        movie = DigestMaker(path,output = output,threshold = "-18",silence_section = "0.1")
    
          
        try:
            info = movie.get_info()
        except OSError:
            print("外部のアプリケーションとの連携が取れていない可能性があります\nお使いのソフト、パソコンを再起動してみてください。")
        else:
            pass
            #info = movie.get_info()
        #print(movie.silence_detect(info))

        starts_ends = movie.silence_detect(info)



        if type(starts_ends) == bool:
            pass
        elif starts_ends == []:
            print(">>無音区間の検出ができませんでした。スレッショルドなどの値を見直してみてください。")
            pass      

        else:
            print(movie.using_parts(starts_ends))
            #print(starts_ends)
            try:
                movie.concatenate_videos()
            except OSError:
                print("出力用のファイルのパスが間違っている可能性があります。")
            else:
                print("動画出力が完了しました。")
