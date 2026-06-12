# ==========================================
# [08_Deque] 양방향 선형 및 원형 덱 구현
# ==========================================

class LinearDeque:
    """선형 덱 (파이썬 내장 리스트 활용)"""
    def __init__(self):
        self.items = []
    def isEmpty(self): return len(self.items) == 0
    def addFront(self, item): self.items.insert(0, item)
    def addRear(self, item): self.items.append(item)
    def deleteFront(self): 
        if not self.isEmpty(): return self.items.pop(0)
    def deleteRear(self): 
        if not self.isEmpty(): return self.items.pop()

class CircularDeque:
    """원형 덱 (고정 배열 기반 원형 구조 확장)"""
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.array = [None] * capacity
        self.front = 0
        self.rear = 0
        
    def isEmpty(self): return self.front == self.rear
    def isFull(self): return (self.rear + 1) % self.capacity == self.front
    
    def addRear(self, item):
        if not self.isFull():
            self.rear = (self.rear + 1) % self.capacity
            self.array[self.rear] = item
            
    def deleteFront(self):
        if not self.isEmpty():
            self.front = (self.front + 1) % self.capacity
            item = self.array[self.front]
            self.array[self.front] = None
            return item
            
    def addFront(self, item):
        if not self.isFull():
            self.array[self.front] = item
            self.front = (self.front - 1 + self.capacity) % self.capacity
            
    def deleteRear(self):
        if not self.isEmpty():
            item = self.array[self.rear]
            self.array[self.rear] = None
            self.rear = (self.rear - 1 + self.capacity) % self.capacity
            return item

if __name__ == "__main__":
    print("--- 원형 덱 구동 테스트 ---")
    cd = CircularDeque(6)
    cd.addRear(1); cd.addRear(2)      # 뒤쪽에 추가
    cd.addFront(9); cd.addFront(8)    # 앞쪽에 추가
    print("원형 덱 내부 배열 구조:", cd.array)
    print("앞에서 추출:", cd.deleteFront())
    print("뒤에서 추출:", cd.deleteRear())
    print("추출 후 내부 배열 구조:", cd.array)
