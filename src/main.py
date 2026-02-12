from board import Board
from solver import solve
from helper import readFile, showResult, validate
import os

file = input("Silahkan masukkan nama file : ")
path = os.path.join("test", file)
board = readFile(path)

if board is None:
    exit(1)

if not validate(board):
    print("Papan wajib berbentuk persegi dan jumlah daerah harus lebih kecil sama dengan sisi")
    exit(1)

found, caseCount, time = solve(board)

if found:
    showResult(board)
    print()
    print(f"Waktu pencarian: {time} ms")
    print(f"Banyak kasus yang ditinjau: {caseCount} kasus")
else:
    print("Solusi tidak ditemukan")