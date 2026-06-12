import tkinter as tk
import time
import threading

# 원형 큐 기반의 BFS 탐색용 자료구조
class CircularQueue:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.array = [None] * capacity
        self.front = 0
        self.rear = 0
    def isEmpty(self): return self.front == self.rear
    def isFull(self): return (self.rear + 1) % self.capacity == self.front
    def enqueue(self, item):
        if not self.isFull():
            self.rear = (self.rear + 1) % self.capacity
            self.array[self.rear] = item
    def dequeue(self):
        if not self.isEmpty():
            self.front = (self.front + 1) % self.capacity
            return self.array[self.front]

class MazeBFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("미로 탐색 (너비 우선 탐색 - BFS)")
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
        title = tk.Label(self.root, text="미로 탐색 (BFS 너비우선)", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="white")
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

        self.status_label = tk.Label(self.root, text="[탐색 시작] 버튼을 누르면 BFS 탐색이 구동됩니다.", font=("Arial", 11), bg="#1a1a1a", fg="#aaaaaa")
        self.status_label.pack(pady=20)

        self.start_btn = tk.Button(self.root, text="탐색 시작", font=("Arial", 12, "bold"), bg="#e65100", fg="white", padx=30, pady=8, command=self.click_start_button, relief="flat")
        self.start_btn.pack(pady=5)

    def click_start_button(self):
        self.start_btn.config(state="disabled", bg="#555555")
        threading.Thread(target=self.solve_maze_bfs, daemon=True).start()

    #  Queue를 사용한 BFS 구현
    def solve_maze_bfs(self):
        q = CircularQueue()
        q.enqueue((0, 1)) # 출발점

        self.status_label.config(text="BFS 너비 우선 탐색 구동 중...", fg="#FFC107")

        while not q.isEmpty():
            curr = q.dequeue()
            x, y = curr

            if self.maze[y][x] == 'x':
                self.status_label.config(text=f"탐색 성공!! 출구({x}, {y})를 찾았습니다.", fg="#4CAF50")
                return True

            if self.maze[y][x] != 'e':
                self.grid_labels[y][x].config(bg="#F44336") # 현재 방문 지점
                time.sleep(0.4)

            if self.maze[y][x] != 'v':
                if self.maze[y][x] != 'e':
                    self.maze[y][x] = 'v'
                    self.grid_labels[y][x].config(bg="#FBC02D") # 탐색 완료 흔적

                # 큐(BFS)는 사방을 동시 확장하므로 순방향 큐 삽입
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.MAZE_SIZE and 0 <= ny < self.MAZE_SIZE:
                        if self.maze[ny][nx] == '0' or self.maze[ny][nx] == 'x':
                            q.enqueue((nx, ny))

        self.status_label.config(text="탐색 실패: 출구를 찾지 못했습니다.", fg="#FF5722")
        return False

if __name__ == "__main__":
    window = tk.Tk()
    app = MazeBFSApp(window)
    window.mainloop()
