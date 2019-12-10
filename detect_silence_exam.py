#3音声を読み込んで、一定の音量以下の部分を計測
from pydub import AudioSegment
from pydub.silence import *

sound = AudioSegment.from_file(計測したい音源のパス, format="音源の形式（ＭＰ3とか）")
chunks = detect_silence(
    sound,

    # 500ms以上の無音がある
    min_silence_len=500,

    # -15dBFS以下で無音とみなす
    silence_thresh=-20, 

    # seek_stepが何なのかはよくわからない
    
    seek_step = 1
)

#ms単位でのリストで帰ってくる
print(str(chunks))
#秒数に直したリスト
for chunk in chunks:
    print(list(map(lambda x:x / 1000,chunk)))