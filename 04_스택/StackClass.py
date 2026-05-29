# ==========================================
# 1. 배열 구조 스택 (ArrayStack)
# ==========================================
class ArrayStack:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.top = -1
        self.array = [None] * capacity

    def isEmpty(self): 
        return self.top == -1

    def isFull(self): 
        return self.top == self.capacity - 1

    def push(self, e):
        """스택이 가득 차 있지 않을 때만 상단에 추가"""
        if not self.isFull():
            self.top += 1
            self.array[self.top] = e
        else:
            print("Stack Overflow: 스택이 가득 찼습니다.")

    def pop(self):
        """스택이 비어있지 않을 때만 상단 원소 삭제 및 반환"""
        if not self.isEmpty():
            item = self.array[self.top]
            self.array[self.top] = None  # 메모리 정리
            self.top -= 1
            return item
        else:
            print("Stack Underflow: 스택이 비어있습니다.")
            return None

    def peek(self):
        """상단 원소를 삭제하지 않고 값만 반환"""
        if not self.isEmpty():
            return self.array[self.top]
        return None

    def display(self, msg="ArrayStack:"):
        # 바닥(0)부터 탑(top)까지 출력
        print(msg, self.array[:self.top + 1])


# ==========================================
# 2. 연결된 구조 스택 (LinkedStack)
# ==========================================
class Node:
    """연결 구조를 위한 노드 클래스"""
    def __init__(self, elem, next=None):
        self.data = elem
        self.link = next

class LinkedStack:
    def __init__(self):
        self.top = None  # 헤드 포인터(가장 최근에 들어온 노드를 가리킴)

    def isEmpty(self): 
        return self.top is None

    # 연결된 구조는 메모리가 허용하는 한 가득 차지 않으므로 isFull은 항상 False
    def isFull(self): 
        return False

    def push(self, e):
        """새 노드를 만들어 기존 top 앞에 링크하고, top을 새 노드로 갱신"""
        self.top = Node(e, self.top)

    def pop(self):
        """가장 상단의 top 노드를 꺼내고 링크를 다음 노드로 이동"""
        if not self.isEmpty():
            item = self.top.data
            self.top = self.top.link  # 다음 노드로 포인터 이동
            return item
        else:
            print("Stack Underflow: 스택이 비어있습니다.")
            return None

    def peek(self):
        if not self.isEmpty():
            return self.top.data
        return None

    def display(self, msg="LinkedStack:"):
        node = self.top
        items = []
        while node is not None:
            items.append(node.data)
            node = node.link
        # 링크드 스택은 출력 시 top이 맨 앞에 보이므로 역순으로 뒤집어 출력하면 배열 구조와 보기 편합니다.
        items.reverse()
        print(msg, items)


# ==========================================
# 3. 인스턴스 생성 및 스택 조작 예제
# ==========================================
if __name__ == "__main__":
    print("=== [1] 배열 구조 스택(ArrayStack) 테스트 ===")
    s1 = ArrayStack(capacity=5)
    s1.push('A')
    s1.push('B')
    s1.push('C')
    s1.display("데이터 Push 후:")  # [A, B, C]
    
    print(f"현재 최상단 원소(peek): {s1.peek()}")
    print(f"Pop 원소: {s1.pop()}")  # C 탈출
    print(f"Pop 원소: {s1.pop()}")  # B 탈출
    s1.display("데이터 Pop 후:")   # [A]
    print("-" * 40)

    print("=== [2] 연결된 구조 스택(LinkedStack) 테스트 ===")
    s2 = LinkedStack()
    s2.push('A')
    s2.push('B')
    s2.push('C')
    s2.display("데이터 Push 후:")  # [A, B, C]
    
    print(f"현재 최상단 원소(peek): {s2.peek()}")
    print(f"Pop 원소: {s2.pop()}")  # C 탈출
    print(f"Pop 원소: {s2.pop()}")  # B 탈출
    s2.display("데이터 Pop 후:")   # [A]
