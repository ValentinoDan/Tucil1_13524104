from core.board import Board
from core.solver import solve
from core.helper import readFile, showResult
import os

file = input("Silahkan masukkan nama file : ")
path = os.path.join("test", file)
board, error = readFile(f"{path}.txt")

if board is None:
    print(f"Error: {error}")
    exit(1)

found, caseCount, time = solve(board)

if found:
    showResult(board)
    print()
    print(f"Waktu pencarian: {time:.2f} ms")
    print(f"Banyak kasus yang ditinjau: {caseCount} kasus")
else:
    print("Solusi tidak ditemukan")