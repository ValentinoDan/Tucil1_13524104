from .board import Board

# Kode warna
colors = {
    'A': 196, 'B': 202, 'C': 226, 'D': 46,   
    'E': 51, 'F': 21, 'G': 93, 'H': 201,  
    'I': 208, 'J': 118, 'K': 39, 'L': 129,
    'M': 220, 'N': 82, 'O': 27, 'P': 200,
    'Q': 214, 'R': 154, 'S': 75, 'T': 141,
    'U': 190, 'V': 49, 'W': 33, 'X': 165,
    'Y': 229, 'Z': 99
}

def validate(board):
    n = board.row
        
    # Jumlah daerah maksimal sama dengan sisi
    place = []
    for i in range(n):
        for j in range(n):
            if board.board[i][j].upper() not in place:
                place.append(board.board[i][j].upper())
    
    if len(place) > n:
        return False
    
    return True

def validateLine(line):
    if not line:
        return False, "Baris kosong tidak diperbolehkan"
    
    for char in line:
        if not char.isalpha():
            return False, f"Karakter wajib berupa alphabet"
    
    return True, ""

# Baca file dengan validasi
def readFile(file):
    try:
        with open(file, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            
            if not lines:
                return None, "File kosong!"
            
            n = len(lines)
            
            # Mengecek tiap baris
            for i, line in enumerate(lines):
                isValid, errorMsg = validateLine(line)
                if not isValid:
                    return None, f"Baris {i+1}: {errorMsg}"
            
            # Mengecek board
            for line in lines:
                if len(line) != n:
                    return None, f"Board harus berbentuk persegi."
            
            # Buat board
            board = Board(n, n)
            for i in range(n):
                for j in range(n):
                    board.board[i][j] = lines[i][j]
            
            # Mengecek jumlah daerah
            if not validate(board):
                return None, f"Jumlah daerah tidak boleh lebih dari {n}."
            
            return board, None

    except FileNotFoundError:
        return None, f"File {file} tidak ditemukan"
    except Exception as e:
        return None, f"Error membaca file: {str(e)}"

# Warna teks
def textColor(letter):
    number = colors.get(letter)
    return f"\033[38;5;{number}m{letter}\033[0m"

# Output solusi
def showResult(board):
    for i in range(board.row):
        for j in range(board.col):
            if board.board[i][j] == "#":
                print("#", end="")
            else:
                print(textColor(board.board[i][j]), end="")
        print()
