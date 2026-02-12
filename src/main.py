from board import Board
from solver import solve
from helper import readFile, showResult
import os

file = input("Silahkan masukkan nama file : ")
path = os.path.join("test", file)
board = readFile(path)

if board is None:
    exit(1)

found, caseCount, time = solve(board)

if found:
    showResult(board)
    print()
    print(f"Waktu pencarian: {time} ms")
    print(f"Banyak kasus yang ditinjau: {caseCount} kasus")
else:
    print("Solusi tidak ditemukan")