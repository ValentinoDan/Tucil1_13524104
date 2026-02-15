from .board import Board
import time

def isValid(pos, letters, n):
    for i in range(n):
        for j in range(i+1, n):
            if pos[i] == pos[j]: # 1 kolom
                return False
            if letters[i][pos[i]] == letters[j][pos[j]]: # tdk bisa di daerah sama
                return False
            if abs(i - j) <= 1 and abs(pos[i] - pos[j]) <= 1: # tdk boleh bersebelahan (diagonal dekat jg)
                return False
            
    return True

def isValidBacktrack(pos, letters, row, col):
    for i in range(row):
        prev = pos[i]

        if prev == col: # cek apakah sudah ada queen ditempat ini
            return False
        
        if letters[i][prev] == letters[row][col]: # cek daerah queen before
            return False
        
        if abs(i - row) <= 1 and abs(prev - col) <= 1: # cek apakah dekat
            return False
    
    return True

def solve(board, update=None, interval=None, backtracks=False):
    n = board.row
    letters = board.board # copy board
    caseCount = 0
    startTime = time.time()

    if backtracks:
        pos = [-1] * n

        def backtrack(row):
            nonlocal caseCount # caseCount global

            if row == n:
                return True
            
            for col in range(n):
                caseCount += 1

                if isValidBacktrack(pos, letters, row, col):
                    pos[row] = col

                    # Live update
                    if update and interval and caseCount % interval == 0:
                        tempBoard = Board(n, n)
                        for i in range(n):
                            for j in range(n):
                                tempBoard.board[i][j] = letters[i][j]
                        
                        for i in range(n):
                            if pos[i] != -1:
                                tempBoard.update(i, pos[i])
                        update(tempBoard)
                        time.sleep(1e-6)

                    if backtrack(row+1):
                        return True
                    
                    pos[row] = -1 # gagal
            
            return False
        
        found = backtrack(0)
        if found:
            for i in range(n):
                board.update(i, pos[i])

            totalTime = (time.time() - startTime) * 1000
            return True, caseCount, totalTime
        
        totalTime = (time.time() - startTime) * 1000
        return False, caseCount, totalTime

    else:
        total = n ** n

        for num in range(total):
            caseCount += 1

            pos = [0] * n # posisi queen
            x = num
            for i in range(n - 1, -1, -1):
                pos[i] = x % n
                x //= n
            
            # Live update
            if update and interval and caseCount % interval == 0:
                tempBoard = Board(n, n)
                for i in range(n):
                    for j in range(n):
                        tempBoard.board[i][j] = letters[i][j]
                
                for i in range(n):
                    tempBoard.update(i, pos[i])
                update(tempBoard)
            
            if isValid(pos, letters, n):
                for i in range(n):
                    board.update(i, pos[i])

                totalTime = (time.time() - startTime) * 1000
                return True, caseCount, totalTime
        
        totalTime = (time.time() - startTime) * 1000
        return False, caseCount, totalTime