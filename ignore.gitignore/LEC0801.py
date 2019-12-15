# ライブラリのインポート
import random
import time
import datetime
# 問1. 1 ～ 10 までの乱数を一度に３つ発生させて、最も小さな値の秒数,処理を止める関数を作成せよ。
def stoptime():
    """ここにこの関数の注釈を書く"""
    # ここに作成せよ
    i1 = random.randint(1,10)
    i2 = random.randint(1,10)
    i3 = random.randint(1,10)
    min_i = min({i1,i2,i3})
    time.sleep(min_i)
    return(min_i)
def stoptime2():
    min_i = set()
    for i in range(3):
        i = random.randint(1,10)
        min_i.add(i)
    min_i =min(min_i)
    return min_i
if __name__ == "__main__":
    print(stoptime2())




if __name__ == "__main__":
    print(stoptime())
# 問2. 1 ～ 10 までの乱数を発生させ、その合計が 100 を超えるまでループするアルゴリズムを作成せよ。
# 毎回合計値を出力し、100 を超えた場合「終了」と知らせよ。
# ここに作成せよ
if __name__ == "__main__":
    
    s = 0
    while s <= 100:
        i = random.randint(1,10)
        s += i
        
        print(s,end = ",")
    print("終了")
# 問3. 現在時刻を表示させよ。

if __name__ == "__main__":
    # ここに作成せよ
    now = datetime.datetime.now()
    print(now)