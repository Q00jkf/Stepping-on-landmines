import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.game_over = False
        self.first_click = True
        self.revealed_count = 0
        
        # 初始化遊戲板
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flagged = [[False for _ in range(cols)] for _ in range(rows)]
        
        # 創建GUI
        self.root = tk.Tk()
        self.root.title("踩地雷 - Minesweeper")
        self.root.resizable(False, False)
        
        # 創建頂部信息欄
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=10)
        
        self.mines_label = tk.Label(self.info_frame, text=f"地雷數: {self.mines}", font=("Arial", 12))
        self.mines_label.pack(side=tk.LEFT, padx=20)
        
        self.restart_button = tk.Button(self.info_frame, text="重新開始", command=self.restart_game, font=("Arial", 12))
        self.restart_button.pack(side=tk.LEFT, padx=20)
        
        self.status_label = tk.Label(self.info_frame, text="左鍵開啟，右鍵標記", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # 創建遊戲板
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=10)
        
        self.buttons = []
        for i in range(rows):
            button_row = []
            for j in range(cols):
                button = tk.Button(self.game_frame, width=3, height=1, font=("Arial", 10, "bold"))
                button.grid(row=i, column=j, padx=1, pady=1)
                button.bind("<Button-1>", lambda event, r=i, c=j: self.left_click(r, c))
                button.bind("<Button-3>", lambda event, r=i, c=j: self.right_click(r, c))
                button_row.append(button)
            self.buttons.append(button_row)
    
    def place_mines(self, exclude_row, exclude_col):
        """在遊戲板上放置地雷，排除首次點擊的位置"""
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # 不在首次點擊位置和已有地雷的位置放置地雷
            if (row != exclude_row or col != exclude_col) and self.board[row][col] != -1:
                self.board[row][col] = -1  # -1 表示地雷
                mines_placed += 1
        
        # 計算每個非地雷格子周圍的地雷數量
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != -1:
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.rows and 0 <= nj < self.cols and self.board[ni][nj] == -1:
                                count += 1
                    self.board[i][j] = count
    
    def left_click(self, row, col):
        """左鍵點擊處理"""
        if self.game_over or self.revealed[row][col] or self.flagged[row][col]:
            return
        
        # 首次點擊時放置地雷
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
        
        # 如果點到地雷
        if self.board[row][col] == -1:
            self.game_over = True
            self.reveal_all_mines()
            self.buttons[row][col].config(bg="red")
            messagebox.showinfo("遊戲結束", "你踩到地雷了！點擊重新開始按鈕再試一次。")
            return
        
        # 揭露格子
        self.reveal_cell(row, col)
        
        # 檢查是否獲勝
        if self.revealed_count == self.rows * self.cols - self.mines:
            self.game_over = True
            messagebox.showinfo("恭喜！", "你成功清除了所有地雷！")
    
    def right_click(self, row, col):
        """右鍵點擊處理（標記/取消標記）"""
        if self.game_over or self.revealed[row][col]:
            return
        
        self.flagged[row][col] = not self.flagged[row][col]
        if self.flagged[row][col]:
            self.buttons[row][col].config(text="🚩", bg="yellow")
        else:
            self.buttons[row][col].config(text="", bg="SystemButtonFace")
    
    def reveal_cell(self, row, col):
        """揭露格子"""
        if self.revealed[row][col]:
            return
        
        self.revealed[row][col] = True
        self.revealed_count += 1
        
        # 設置格子顏色和文字
        if self.board[row][col] == 0:
            self.buttons[row][col].config(text="", bg="lightgray")
            # 如果是空格子，自動揭露周圍的格子
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = row + di, col + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        if not self.revealed[ni][nj] and not self.flagged[ni][nj]:
                            self.reveal_cell(ni, nj)
        else:
            # 根據周圍地雷數量設置顏色
            colors = ["", "blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]
            self.buttons[row][col].config(
                text=str(self.board[row][col]),
                bg="lightgray",
                fg=colors[self.board[row][col]]
            )
    
    def reveal_all_mines(self):
        """揭露所有地雷"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    self.buttons[i][j].config(text="💣", bg="red")
    
    def restart_game(self):
        """重新開始遊戲"""
        self.game_over = False
        self.first_click = True
        self.revealed_count = 0
        
        # 重置遊戲板
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 重置按鈕
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(text="", bg="SystemButtonFace")
    
    def run(self):
        """運行遊戲"""
        self.root.mainloop()

# 創建不同難度的遊戲
def create_game():
    """創建遊戲選擇界面"""
    root = tk.Tk()
    root.title("踩地雷 - 選擇難度")
    root.geometry("300x200")
    root.resizable(False, False)
    
    tk.Label(root, text="選擇遊戲難度", font=("Arial", 16)).pack(pady=20)
    
    def start_game(rows, cols, mines):
        root.destroy()
        game = Minesweeper(rows, cols, mines)
        game.run()
    
    tk.Button(root, text="初級 (9x9, 10雷)", 
              command=lambda: start_game(9, 9, 10),
              font=("Arial", 12), width=20, height=2).pack(pady=5)
    
    tk.Button(root, text="中級 (16x16, 40雷)", 
              command=lambda: start_game(16, 16, 40),
              font=("Arial", 12), width=20, height=2).pack(pady=5)
    
    tk.Button(root, text="高級 (16x30, 99雷)", 
              command=lambda: start_game(16, 30, 99),
              font=("Arial", 12), width=20, height=2).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_game()