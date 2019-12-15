import numpy as np

white = 1
black = -1
blank = 0
tablesize = 8

class Board(object):
    # 初期設定
    def __init__(self):
        self.cell = np.zeros((tablesize,tablesize))
        self.cell = self.cell.astype(int)
        self.cell[3][3] = self.cell[4][4] = 1
        self.cell[3][4] = self.cell[4][3] = -1
        self.current = black
        self.pass_count = 0
        self.turn = 1

    def turnchange(self):  #  ＊
        self.current*= -1


    

