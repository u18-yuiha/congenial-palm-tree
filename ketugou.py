#動画の分割
#moviepyをインポート
from moviepy.editor import *
#動画結合用のリスト
merge_list = [[1061, 1653], [5270, 6028], [7595, 7768], [12790, 13823], [14899, 15104], [16919, 19451], [20855, 22047], [26737, 27457], [29966, 30444], [31373, 32323], [38683, 39553], [42619, 45241], [45937, 47081], [47975, 47985], [48683, 49778], [50594, 53645], [55714, 55962], [57957, 58273], [63274, 63310], [63874, 64466]]
name = rf'C:\Users\AraiAkihiko\Videos\Exp\ダイジェストメーカ―サンプル.mp4' # 入力動画
video = VideoFileClip(name) 
clips = {}
count = 0
for i in range(len(merge_list)):
    clips[count] = video.subclip(merge_list[i][0]/1000,merge_list[i][1]/1000)
    count += 1

videos = [clips[i] for i in range(count)]
result = concatenate(videos)
result.write_videofile(rf"C:\Users\AraiAkihiko\Videos\Exp\result.mp4")