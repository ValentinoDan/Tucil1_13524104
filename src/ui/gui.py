import flet as ft
import os
from PIL import Image, ImageDraw, ImageFont
from core.board import Board
from core.solver import solve
from core.helper import readFile, validate, validateLine

def main(page: ft.Page):
    page.title = "Queen's Linkedin Game Solver"
    page.window.width = 1050
    page.window.height = 750
    page.padding = 30
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.DARK
    
    # Text field untuk input board
    boardInput = ft.TextField(
        cursor_color=ft.Colors.BLUE_200,
        multiline=True,
        max_lines=15,
        min_lines=9,
        width=350,
        label="Input Board",
        hint_text="Masukkan board atau load dari file",
        border_color=ft.Colors.BLUE_400,
        focused_border_color=ft.Colors.BLUE_700,
        border_radius=5
    )
    
    # Warna untuk tiap daerah
    colors = {
        'A': '#EF4444', 'B': '#F97316', 'C': '#F59E0B', 'D': '#EAB308',
        'E': '#84CC16', 'F': '#22C55E', 'G': '#10B981', 'H': '#14B8A6',
        'I': '#06B6D4', 'J': '#0EA5E9', 'K': '#3B82F6', 'L': '#6366F1',
        'M': '#8B5CF6', 'N': '#A855F7', 'O': '#D946EF', 'P': '#EC4899',
        'Q': '#F43F5E', 'R': '#FB7185', 'S': '#FDA4AF', 'T': '#FCA5A5',
        'U': '#FCD34D', 'V': '#BEF264', 'W': '#86EFAC', 'X': '#5EEAD4',
        'Y': '#7DD3FC', 'Z': '#A5B4FC'
    }
    
    # Buat board grid
    def createBoardGrid(board):
        n = board.row
        cellSize = min(40, 380 // n) 
        
        grid = ft.Column(spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        for i in range(n):
            row = ft.Row(spacing=2, alignment=ft.MainAxisAlignment.CENTER)
            for j in range(n):
                letter = board.board[i][j]
                isQueen = (letter == '#')
                
                if isQueen:
                    bgcolor = "#FFD700"  
                    content = ft.Text("👑", size=cellSize*0.6, weight=ft.FontWeight.BOLD)
                else:
                    bgcolor = colors.get(letter.upper(), "#94A3B8")
                    content = ft.Text(size=cellSize*0.5, weight=ft.FontWeight.BOLD)
                
                cell = ft.Container(
                    content=content,
                    width=cellSize,
                    height=cellSize,
                    bgcolor=bgcolor,
                    border_radius=3,
                    alignment=ft.alignment.center,
                )
                row.controls.append(cell)
            grid.controls.append(row)
        
        return grid
    
    # Grid Board
    boardDisplay = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    
    # Text Result
    result = ft.Text(size=12, selectable=True, weight=ft.FontWeight.W_500, text_align=ft.TextAlign.CENTER)
    
    # Text untuk nama file
    fileName = ft.Text("", size=12, color=ft.Colors.GREY_400)

    # Result container
    resultContainer = ft.Container(
        content=ft.Column([
            boardDisplay,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            result
        ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        padding=15,
        border_radius=8,
        bgcolor=ft.Colors.BLUE_100,
        border=ft.border.all(1, ft.Colors.GREY_300),
        width=480,
        height=550,
        animate=ft.Animation(300, "ease")
    )

    # checkbox backtrack
    checkbox = ft.Checkbox(label = "Enable Backtracking (Faster & Recommended)", value = False)

    def validateBoard():
        if not boardInput.value or not boardInput.value.strip():
            return None, "Silakan masukkan konfigurasi board terlebih dahulu!"
            
        lines = boardInput.value.strip().split("\n")
        n = len(lines)
        
        # Validasi tiap baris
        for i, line in enumerate(lines):
            isValid, errorMsg = validateLine(line)
            if not isValid:
                return None, f"Format board tidak valid!\nBaris {i+1}: {errorMsg}"
        
        # Cek persegi
        for line in lines:
            if len(line) != n:
                return None, "Format board tidak valid!\nBoard harus berbentuk persegi."
        
        # Buat board
        board = Board(n, n)
        try:
            for i in range(n):
                for j in range(n):
                    board.board[i][j] = lines[i][j]
        except IndexError:
            return None, "Format board tidak valid!"
        
        # Validasi jumlah daerah
        if not validate(board):
            return None, "Format board tidak valid!"
        
        return board, None

    def exportTxt(e):
        board, error = validateBoard()
        boardDisplay.controls.clear()
        if error:
            result.value = error
            resultContainer.bgcolor = "#78350F"
            resultContainer.border = ft.border.all(1, "#F59E0B")
            result.color = "#FCD34D"
            page.update()
            return
        folder = "result" # folder save output
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        files = os.listdir(folder)
        found, count, time = solve(board)
        filepath = os.path.join(folder, f"result{len(files) + 1}.txt")
        
        with open(filepath, "w") as f:
            if found:
                for i in range(board.row):
                    for j in range(board.col):
                            f.write(board.board[i][j])
                    f.write("\n")
                f.write("\n")
            else:
                f.write("Solusi tidak ditemukan\n")
            f.write(f"Waktu pencarian: {time:.2f} ms\n")
            f.write(f"Banyak kasus yang ditinjau: {count} kasus\n")
        
        result.value = f"Berhasil diexport ke result{len(files) + 1}.txt"
        resultContainer.bgcolor = "#064E3B"
        resultContainer.border = ft.border.all(1, "#10B981")
        result.color = "#6EE7B7"
        page.update()

    def exportImage(e):
        board, error = validateBoard()
        boardDisplay.controls.clear()
        if error:
            result.value = error
            resultContainer.bgcolor = "#78350F"
            resultContainer.border = ft.border.all(1, "#F59E0B")
            result.color = "#FCD34D"
            page.update()
            return
        
        n = board.row
        
        found, count, time = solve(board, None, None, backtracks=True)
        if not found:
            result.value = "Solusi tidak ditemukan, tidak bisa di-export"
            resultContainer.bgcolor = "#7F1D1D"
            resultContainer.border = ft.border.all(1, "#EF4444")
            result.color = "#FCA5A5"
            page.update()
            return
        
        grid = [[0 for _ in range(n)] for _ in range(n)]
        queens = []
        for i in range(n):
            for j in range(n):
                if board.board[i][j] != "#":
                    grid[i][j] = colors.get(board.board[i][j].upper(), "#94A3B8")
                else:
                    grid[i][j] = "#FFD700"
                    queens.append((i, j))

        cell = 80
        crown = Image.open("font/crown.png").resize((cell // 2, cell // 2))
        img = Image.new("RGB", (n * cell, n * cell))
        draw = ImageDraw.Draw(img)

        for i in range(n):
            for j in range(n):
                x1 = j * cell
                y1 = i * cell
                x2 = x1 + cell
                y2 = y1 + cell

                draw.rectangle([x1, y1, x2, y2], fill=grid[i][j], outline="black")

                if (i, j) in queens:
                    img.paste(crown, (int(x1 + cell/3.7), y1 + cell//4), crown)

        folder = "result"
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        img.save("result/game.png")
        
        result.value = "Berhasil diexport ke game.png"
        resultContainer.bgcolor = "#064E3B"
        resultContainer.border = ft.border.all(1, "#10B981")
        result.color = "#6EE7B7"
        page.update()

    # Load file
    def loadFile(e: ft.FilePickerResultEvent):
        if e.files:
            filePath = e.files[0].path
            fileName.value = f"File: {e.files[0].name}"
            
            board, error = readFile(filePath)
            if board:
                lines = []
                for i in range(board.row):
                    lines.append("".join(board.board[i]))
                boardInput.value = "\n".join(lines)
                boardDisplay.controls.clear()
                result.value = "File berhasil dimuat"
                resultContainer.bgcolor = "#064E3B"
                resultContainer.border = ft.border.all(1, "#10B981")
                result.color = "#6EE7B7"
            else:
                boardDisplay.controls.clear()
                result.value = f"Error: {error}"
                resultContainer.bgcolor = "#7F1D1D"
                resultContainer.border = ft.border.all(1, "#EF4444")
                result.color = "#FCA5A5"
            page.update()
    
    filePicker = ft.FilePicker(on_result=loadFile)
    page.overlay.append(filePicker)

    def pickFile(e):
        filePicker.pick_files(
            allowed_extensions=["txt"],
            dialog_title="Pilih file konfigurasi"
        )
    
    # Solve
    def solves(e):
        board, error = validateBoard()
        if error:
            boardDisplay.controls.clear()
            result.value = error
            resultContainer.bgcolor = "#78350F"
            resultContainer.border = ft.border.all(1, "#F59E0B")
            result.color = "#FCD34D"
            page.update()
            return
        
        backtracks = checkbox.value # ambil value dari checkbox

        n = board.row
        boardDisplay.controls.clear()
        result.value = "Sedang mencari solusi..."
        resultContainer.bgcolor = "#1E3A8A"  
        result.color = ft.Colors.WHITE
        page.update()
        
        # Live update
        def updateProgress(tempBoard):
            boardDisplay.controls.clear()
            boardDisplay.controls.append(ft.Text("Mencari solusi...", size=14, weight=ft.FontWeight.BOLD, color="#60A5FA"))
            boardDisplay.controls.append(createBoardGrid(tempBoard))
            page.update()
        
        found, caseCount, time = solve(board, update=updateProgress, interval=1.5, backtracks=backtracks)

        if found:
            boardDisplay.controls.clear()
            boardDisplay.controls.append(
                ft.Text("Solusi Ditemukan!", size=16, weight=ft.FontWeight.BOLD, color="#10B981")
            )
            boardDisplay.controls.append(createBoardGrid(board))
            
            result.value = f"Waktu pencarian: {time:.2f} ms\nKasus ditinjau: {caseCount} kasus"
            resultContainer.bgcolor = "#064E3B"
            resultContainer.border = ft.border.all(1, "#10B981")
            result.color = "#6EE7B7"
        else:
            boardDisplay.controls.clear()
            boardDisplay.controls.append(
                ft.Text("Solusi Tidak Ditemukan", size=16, weight=ft.FontWeight.BOLD, color="#EF4444")
            )
            result.value = f"Coba dengan konfigurasi board yang berbeda.\nWaktu pencarian: {time:.2f} ms\nKasus ditinjau: {caseCount} kasus"
            resultContainer.bgcolor = "#7F1D1D"
            resultContainer.border = ft.border.all(1, "#EF4444")
            result.color = "#FCA5A5"

        page.update()

    # UI
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Queen's Linkedin Game Solver",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                ),
                ft.Divider(height=20, color=ft.Colors.BLUE_200),
                
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Input Board:", size=16, color="#E2E8F0", weight=ft.FontWeight.BOLD),
                            boardInput,
                            ft.Row([
                                ft.ElevatedButton(
                                    "Load dari File",
                                    icon=ft.Icons.UPLOAD_FILE,
                                    on_click=pickFile,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.BLUE_600
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Solve",
                                    icon=ft.Icons.PLAY_ARROW,
                                    on_click=solves,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.GREEN_600
                                    )
                                ),
                            ], spacing=10),
                            ft.Row([
                                ft.ElevatedButton(
                                    "Export TXT",
                                    icon=ft.Icons.SHARE,
                                    on_click=exportTxt,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.PURPLE_600
                                    )
                                ),
                                ft.ElevatedButton(
                                    "Export Image",
                                    icon=ft.Icons.IMAGE,
                                    on_click=exportImage,
                                    style=ft.ButtonStyle(
                                        color=ft.Colors.WHITE,
                                        bgcolor=ft.Colors.PINK_600
                                    )
                                ),
                            ], spacing=10),
                            checkbox,
                            fileName,
                        ], spacing=15),
                        padding=20,
                        border_radius=10,
                        bgcolor="#1E293B"
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Hasil:", size=16, color=ft.Colors.WHITE54, weight=ft.FontWeight.BOLD),
                            resultContainer,
                        ], spacing=10),
                        padding=20,
                    )
                ], spacing=20, scroll=ft.ScrollMode.AUTO),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLACK38,
            border_radius=15,
            padding=20,
        )
    )