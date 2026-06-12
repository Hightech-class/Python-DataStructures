# ==========================================
# [07_Queue] 선형 큐 및 원형 큐 클래스 구현
# ==========================================

class LinearQueue:
    """선형 큐 (배열 기반)"""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.queue = []
        
    def isEmpty(self): return len(self.queue) == 0
    def isFull(self): return len(self.queue) == self.capacity
    
    def enqueue(self, item):
        if not self.isFull():
            self.queue.append(item)
            
    def dequeue(self):
        if not self.isEmpty():
            return self.queue.pop(0) # 맨 앞 데이터 추출
        return None

class CircularQueue:
    """원형 큐 (고정 크기 링 버퍼)"""
    def __init__(self, capacity=8):
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
            item = self.array[self.front]
            self.array[self.front] = None
            return item
        return None

# 검증 및 실행 테스트
if __name__ == "__main__":
    print("--- 1. 선형 큐 테스트 ---")
    lq = LinearQueue(3)
    lq.enqueue('A'); lq.enqueue('B'); lq.enqueue('C')
    print("선형 큐 추출:", lq.dequeue())
    print("선형 큐 추출:", lq.dequeue())
    
    print("\n--- 2. 원형 큐 테스트 ---")
    cq = CircularQueue(5)
    cq.enqueue(10); cq.enqueue(20); cq.enqueue(30)
    print("원형 큐 상태 배열:", cq.array)
    print("원형 큐 추출:", cq.dequeue())
    print("원형 큐 추출:", cq.dequeue())
    cq.enqueue(40)
    print("원형 큐 상태 배열(원소 추가 후):", cq.array)
