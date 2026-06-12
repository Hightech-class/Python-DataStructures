import tkinter as tk
import time
import threading

class Stack:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.array = [None] * capacity
        self.top = -1
    def isEmpty(self): return self.top == -1
    def push(self, e):
        if self.top < self.capacity - 1:
            self.top += 1
            self.array[self.top] = e
    def pop(self):
        if not self.isEmpty():
            item = self.array[self.top]
            self.top -= 1
            return item

class MazeStrategicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("미로 탐색 (전략적 가중치 탐색)")
        self.root.geometry("450x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a1a")

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
        title = tk.Label(self.root, text="미로 탐색 (전략적 우선탐색)", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
        title.pack(pady=20)

        board_frame = tk.Frame(self.root, bg="#2d2d2d", padx=10, pady=10)
        board_frame.pack(pady=10)

        for y in range(self.MAZE_SIZE):
            for x in range(self.MAZE_SIZE):
                val = self.maze[y][x]
                bg_color = "#263238" if val == '1' else "#2196F3" if val == 'e' else "#4CAF50" if val == 'x' else "#121212"
                lbl = tk.Label(board_frame, text=val if val in ['e', 'x'] else "", font=("Arial", 12, "bold"), width=4, height=2, bg=bg_color, fg="white")
                lbl.grid(row=y, column=x, padx=3, pady=3)
                self.grid_labels[y][x] = lbl

        self.status_label = tk.Label(self.root, text="[탐색 시작] 버튼을 누르면 전략 탐색이 구동됩니다.", font=("Arial", 11), bg="#1a1a1a", fg="#aaaaaa")
        self.status_label.pack(pady=20)

        self.start_btn = tk.Button(self.root, text="탐색 시작", font=("Arial", 12, "bold"), bg="#004d40", fg="white", padx=30, pady=8, command=self.click_start_button, relief="flat")
        self.start_btn.pack(pady=5)

    def click_start_button(self):
        self.start_btn.config(state="disabled", bg="#555555")
        threading.Thread(target=self.solve_maze_strategic, daemon=True).start()

    # ★ 핵심 수정 파트: 출구(5, 3) 방향에 최적화된 가중치 방향 정렬 전략
    def solve_maze_strategic(self):
        s = Stack()
        s.push((0, 1))
        exit_x, exit_y = 5, 3 # 출구 좌표 목적지 고정

        self.status_label.config(text="전략적 방향 탐색 구동 중...", fg="#FFC107")

        while not s.isEmpty():
            curr = s.pop()
            x, y = curr

            if self.maze[y][x] == 'x':
                self.status_label.config(text=f"탐색 성공!! 출구({x}, {y})를 찾았습니다.", fg="#4CAF50")
                return True

            if self.maze[y][x] != 'e':
                self.grid_labels[y][x].config(bg="#F44336")
                time.sleep(0.4)

            if self.maze[y][x] != 'v':
                if self.maze[y][x] != 'e':
                    maze_val = 'v'
                    self.maze[y][x] = 'v'
                    self.grid_labels[y][x].config(bg="#FBC02D")

                # [전략 연산] 출구와의 거리가 가까운 유망한 방향을 먼저 스택에 쌓는 정렬 기술
                neighbors = []
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.MAZE_SIZE and 0 <= ny < self.MAZE_SIZE:
                        if self.maze[ny][nx] == '0' or self.maze[ny][nx] == 'x':
                            # 맨해튼 거리(목적지까지의 잔여 거리) 계산
                            distance = abs(nx - exit_x) + abs(ny - exit_y)
                            neighbors.append((nx, ny, distance))
                
                # 거리가 먼 것을 스택에 먼저 넣어야 pop() 할 때 거리가 가장 가까운 유망 경로가 먼저 튀어나옴
                neighbors.sort(key=lambda item: item[2], reverse=True)
                for nx, ny, _ in neighbors:
                    s.push((nx, ny))

        self.status_label.config(text="탐색 실패: 출구를 찾지 못했습니다.", fg="#FF5722")
        return False

if __name__ == "__main__":
    window = tk.Tk()
    app = MazeStrategicApp(window)
    window.mainloop()
