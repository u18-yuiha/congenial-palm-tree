"""
import ffmpeg
 
(
crfは動画の画質を調整する値(0~51)。小さい値ほど画質が良くなる。18~28辺りが妥当
presetは圧縮率に対する特定のエンコード速度を提供するオプションの集まり。遅いものほど圧縮率がよい。
「ultrafast,superfasut,veryfast,faster,fast,medium,slow,slower,veryslow,placebo」(エンコード速度の降順)
何も設定しないと、mediumとなる。
    ffmpeg
    .input(rf"音声を抽出したい動画のパス")
    .output("抽出した音声の保存先のパス.音声の形式(mp3,wav等)", acodec = "音声の形式(mp3,wav等)", crf=23, preset='slow',vcodec = "vn")
    .run()
)
"""