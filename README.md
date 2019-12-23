# congenial-palm-tree >> README.md
git init
git add README.md
git commiti -mfirst commit
git remote add origin https://github.com/u18-yuiha/congenial-palm-tree.git
git push -u origin master
echo # congenial-palm-tree
# このプログラムはffmpeg,ffmpeg-python,pydub,moviepyをインストールしてから使ってください
# ffmpegのインストールの手順【参考）
https://fukatsu.tech/windows-ffmpeg
# このプログラムができること
入力された動画から一定の音量以下の部分を検出して、その部分をカットした動画を出力します。

＊動画をカットする際に「プツッ」としたノイズが乗る場合があります。
気になる場合は動画編集ソフトなどでBGMを追加してあげてください。
# このプログラムの使い方。
path：入力する動画のパス（パスに「。」や「、」空白などが含まれていると、エラーを起こす可能性がある。）
output：出力する動画のパス（パスに「。」や「、」空白などが含まれていると、エラーを起こす可能性がある。）
threshold：閾値。この音量以下の部分を無音とみなす値。（－10～－40辺りを推奨）
silence_section：無音の部分がsilence_section秒あったらそれを無音区間とする（0.4～2.0辺りを推奨）
FPS：FPSは高いほど画質が良くなる。しかし処理が重くなる（15～60の間が推奨）

を入力して、実行します。



