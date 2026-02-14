class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = [["" for _ in range(col)] for _ in range(row)]
    
    # Update 1 posisi di board menjadi Queen
    def update(self, row, col):
        self.board[row][col] = "#"

    # Remove Queen (jadi kosong)
    def remove(self, row, col):
        self.board[row][col] = ""