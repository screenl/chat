
class Board:
    def __init__(self) -> None:
        self.board=[[0 for i in range(10)] for j in range(10)]
        self.last = ''
    def place(self,x,y,player):
        if self.board[x][y] == 0:
            self.board[x][y]=player
        else:
            raise Exception("Invalid Move")

    def check(self):
        winner = -1
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] == self.board[i+4][j] and self.board[i][j] != 0:
                    winner = self.board[i][j]
                elif self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] == self.board[i][j+4] and self.board[i][j] != 0:
                    winner = self.board[i][j]
                elif self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.board[i+4][j+4] and self.board[i][j] != 0:
                    winner = self.board[i][j]
        return winner   

    def disp(self):
        for i in self.board:
            print(i)

def main():
    chess = Board()
    while chess.check() == -1:
        p = input()
        x,y,player = p.split()
        chess.place(int(x),int(y),player)
        chess.disp()

if __name__ == '__main__':
    main()