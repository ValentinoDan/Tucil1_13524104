from board import Board

# Kode warna
colors = {
    'A': 196,  # merah terang
    'B': 202,  # orange
    'C': 226,  # kuning terang
    'D': 46,   # hijau terang
    'E': 51,   # cyan terang
    'F': 21,   # biru terang
    'G': 93,   # ungu
    'H': 201,  # pink
    'I': 208,
    'J': 118,
    'K': 39,
    'L': 129,
    'M': 220,
    'N': 82,
    'O': 27,
    'P': 200,
    'Q': 214,
    'R': 154,
    'S': 75,
    'T': 141,
    'U': 190,
    'V': 49,
    'W': 33,
    'X': 165,
    'Y': 229,
    'Z': 99
}

# Baca file
def readFile(file):
    try:
        with open(file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            n = len(lines)

            board = Board(n, n)
            for i in range(n):
                for j in range(n):
                    board.board[i][j] = lines[i][j]
            
            return board

    except FileNotFoundError:
        print(f"Error: File {file} tidak ditemukan")
        return None

def validate(board):
    n = board.row

    # Wajib persegi
    for line in board.board:
        if len(line) != n:
            return False
        
    # Jumlah daerah maksimal sama dengan sisi
    place = []
    for i in range(n):
        for j in range(n):
            if board.board[i][j] not in place:
                place.append(board.board[i][j])
    
    if len(place) > n:
        return False
    
    return True

# Warna teks
def textColor(letter):
    number = colors.get(letter)
    return f"\033[38;5;{number}m{letter}\033[0m"

# Output solusi
def showResult(board):
    for i in range(board.row):
        for j in range(board.col):
            if board.board[i][j] == "Q":
                print("#", end="")
            else:
                print(textColor(board.board[i][j]), end="")
        print()

