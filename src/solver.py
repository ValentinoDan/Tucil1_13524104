from board import Board
import time

def isValid(pos, letters, n):
    for i in range(n):
        for j in range(i+1, n):
            if pos[i] == pos[j]: # 1 kolom
                return False
            if letters[i][pos[i]] == letters[j][pos[j]]: # tdk bisa di daerah sama
                return False
            if abs(i - j) <= 1 and abs(pos[i] - pos[j]) <= 1: # tdk boleh bersebelahan (diagonal jg)
                return False
            
    return True
            

def solve(board):
    n = board.row
    letters = board.board
    pos = list(range(n)) 
    caseCount = 0
    startTime = time.time()

    while True:
        caseCount += 1
        if isValid(pos, letters, n):
            for i in range(n):
                board.update(i, pos[i])

            totalTime = (time.time() - startTime) * 1000
            return True, caseCount, totalTime
        
        idx = n - 1
        while idx >= 0:
            pos[idx] += 1
            if pos[idx] < n:
                break
            else:
                pos[idx] = 0 # reset ke 0
                idx -= 1

        if idx < 0:
            break
    
    totalTime = (time.time() - startTime) * 1000
    return False, caseCount, totalTime