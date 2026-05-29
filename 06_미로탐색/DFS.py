import tkinter as tk
import time
import threading

# ==========================================
# 1. 원본 소스코드의 Stack 구조 유지 (100% 동일)
# ==========================================
class Stack:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.array = [None] * capacity
        self.top = -1

    def isEmpty(self): return self.top == -1
    def isFull(self): return self.top == self.capacity - 1

    def push(self, e):
        if not self.isFull():
            self.top += 1
            self.array[self.top] = e

    def pop(self):
        if not self.isEmpty():
            item = self.array[self.top]
            self.array[self.top] = None
            self.top -= 1
            return item
        return None


# ==========================================
# 2. 렌더링 오류가 절대 없는 순정 Tkinter GUI 구현
# ==========================================
class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("미로 탐색")
        self.root.geometry("450x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")  # 다크 테마

        # 원본 소스코드의 6x6 미로 데이터
        self.maze = [
            ['1', '1', '1', '1', '1', '1'],
            ['e', '0', '0', '0', '0', '1'],
            ['1', '0', '1', '0', '1', '1'],
            ['1', '1', '1', '0', '0', 'x'],
            ['1', '1', '1', '0', '1', '1'],
            ['1', '1', '1', '1', '1', '1']
        ]
        self.MAZE_SIZE = 6
        self.grid_labels = [[None for _ in range(6)] for _ in range(6)]
        
        self.setup_ui()

    def setup_ui(self):
        # 타이틀 표시
        title = tk.Label(self.root, text="미로 탐색 (DFS 시각화)", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
        title.pack(pady=20)

        # 미로판 프레임 고정
        board_frame = tk.Frame(self.root, bg="#2d2d2d", padx=10, pady=10)
        board_frame.pack(pady=10)

        # 격자판 그리기
        for y in range(self.MAZE_SIZE):
            for x in range(self.MAZE_SIZE):
                val = self.maze[y][x]
                if val == '1': bg_color = "#263238"    # 벽 (진회색)
                elif val == 'e': bg_color = "#2196F3"  # 출발 (파란색)
                elif val == 'x': bg_color = "#4CAF50"  # 출구 (초록색)
                else: bg_color = "#121212"             # 길 (검은색)

                lbl = tk.Label(
                    board_frame, 
                    text=val if val in ['e', 'x'] else "", 
                    font=("Arial", 12, "bold"),
                    width=4, 
                    height=2, 
                    bg=bg_color, 
                    fg="white",
                    relief="flat"
                )
                lbl.grid(row=y, column=x, padx=3, pady=3)
                self.grid_labels[y][x] = lbl

        # 상태 설명창
        self.status_label = tk.Label(
            self.root, 
            text="[탐색 시작] 버튼을 누르면 DFS 탐색이 구동됩니다.", 
            font=("Arial", 11), 
            bg="#1a1a1a", 
            fg="#aaaaaa"
        )
        self.status_label.pack(pady=20)

        # 시작 버튼
        self.start_btn = tk.Button(
            self.root, 
            text="탐색 시작", 
            font=("Arial", 12, "bold"), 
            bg="#0d47a1", 
            fg="white", 
            padx=30, 
            pady=8,
            command=self.click_start_button,
            relief="flat",
            cursor="hand2"
        )
        self.start_btn.pack(pady=5)

    def click_start_button(self):
        self.start_btn.config(state="disabled", bg="#555555")
        # 애니메이션이 부드럽게 갱신되도록 멀티스레드로 DFS 알고리즘 호출
        threading.Thread(target=self.solve_maze_dfs, daemon=True).start()

    # ==========================================
    # 3. 원본 소스코드의 DFS 탐색 알고리즘 (100% 동일)
    # ==========================================
    def solve_maze_dfs(self):
        s = Stack()
        start_x, start_y = 0, 1
        s.push((start_x, start_y))

        self.status_label.config(text="미로 탐색 알고리즘 구동 중...", fg="#FFC107")

        while not s.isEmpty():
            curr = s.pop()
            x, y = curr

            if self.maze[y][x] == 'x':
                self.status_label.config(text=f"탐색 성공!! 출구({x}, {y})를 찾았습니다.", fg="#4CAF50")
                self.grid_labels[y][x].config(bg="#4CAF50")
                return True

            if self.maze[y][x] != 'e':
                self.grid_labels[y][x].config(bg="#F44336") # 현재 탐색점 (빨간색)
                time.sleep(0.4) 

            if self.maze[y][x] != 'v':
                if self.maze[y][x] != 'e':
                    self.maze[y][x] = 'v'
                    self.grid_labels[y][x].config(bg="#FBC02D") # 지나온 길 (노란색)

                # 상하좌우 탐색 규칙 원본 그대로 적용
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.MAZE_SIZE and 0 <= ny < self.MAZE_SIZE:
                        if self.maze[ny][nx] == '0' or self.maze[ny][nx] == 'x':
                            s.push((nx, ny))

        self.status_label.config(text="탐색 실패: 출구를 찾지 못했습니다.", fg="#FF5722")
        return False


if __name__ == "__main__":
    window = tk.Tk()
    app = MazeApp(window)
    window.mainloop()
