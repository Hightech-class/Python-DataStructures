# ==========================================
# [09_PriorityQueue] 우선순위 큐 클래스 구현
# ==========================================

class PriorityQueue:
    """우선순위가 가장 높은 원소가 먼저 나오는 큐 (정렬 기반)"""
    def __init__(self):
        self.items = []
        
    def isEmpty(self): return len(self.items) == 0
    
    def enqueue(self, item, priority):
        # (아이템, 우선순위 정수) 튜플 형태로 삽입
        # 여기서는 숫자가 작을수록 우선순위가 높다고 가정합니다.
        self.items.append((item, priority))
        # 삽입할 때마다 우선순위 기준 정렬 (내림차순 정렬 후 pop()하면 가장 작은 원소가 나옴)
        self.items.sort(key=lambda x: x[1], reverse=True)
        
    def dequeue(self):
        if not self.isEmpty():
            return self.items.pop() # 가장 높은 우선순위 원소 반환
        return None

if __name__ == "__main__":
    print("--- 우선순위 큐 테스트 (숫자가 작을수록 우선순위 높음) ---")
    pq = PriorityQueue()
    pq.enqueue("응급환자 A", 3)
    pq.enqueue("일반환자 B", 5)
    pq.enqueue("최고 중증환자 C", 1)
    
    print("처리 순서 1:", pq.dequeue())
    print("처리 순서 2:", pq.dequeue())
    print("처리 순서 3:", pq.dequeue())
