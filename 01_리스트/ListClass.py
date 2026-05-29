# ==========================================
# 1. 배열 구조 리스트 (ArrayList)
# ==========================================
class ArrayList:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.items = [None] * capacity  # 고정 배열
        self.size_count = 0

    def isEmpty(self): return self.size_count == 0
    def isFull(self): return self.size_count == self.capacity

    def insert(self, pos, e):
        if not self.isFull() and 0 <= pos <= self.size_count:
            # 뒤에서부터 pos까지 한 칸씩 밀기 (Shifting)
            for i in range(self.size_count, pos, -1):
                self.items[i] = self.items[i-1]
            self.items[pos] = e
            self.size_count += 1

    def delete(self, pos):
        if not self.isEmpty() and 0 <= pos < self.size_count:
            item = self.items[pos]
            # pos부터 앞으로 한 칸씩 당기기
            for i in range(pos, self.size_count - 1):
                self.items[i] = self.items[i+1]
            self.size_count -= 1
            return item

    def display(self):
        print(f"ArrayList: {self.items[:self.size_count]}")


# ==========================================
# 2. 연결된 구조 리스트 (SinglyLinkedList)
# ==========================================
class Node:
    """연결 리스트를 구성하는 노드 클래스"""
    def __init__(self, elem, next=None):
        self.data = elem
        self.link = next

class SinglyLinkedList:
    def __init__(self):
        self.head = None  # 시작 노드를 가리키는 포인터

    def isEmpty(self): 
        return self.head is None

    def getNode(self, pos):
        """해당 위치(pos)의 노드를 찾아 반환하는 보조 메서드"""
        if pos < 0: 
            return None
        node = self.head
        for _ in range(pos):
            if node is None:
                break
            node = node.link
        return node

    def insert(self, pos, e):
        """특정 위치(pos)에 새 원소 삽입"""
        if pos == 0:  # 맨 앞에 삽입하는 경우
            self.head = Node(e, self.head)
        else:
            prev = self.getNode(pos - 1)  # 삽입할 위치의 이전 노드를 찾음
            if prev is not None:
                prev.link = Node(e, prev.link)

    def delete(self, pos):
        """특정 위치(pos)의 원소 삭제 및 반환"""
        if self.isEmpty() or pos < 0:
            return None
        
        if pos == 0:  # 맨 앞 원소를 삭제하는 경우
            item = self.head.data
            self.head = self.head.link
            return item
        else:
            prev = self.getNode(pos - 1)
            if prev is not None and prev.link is not None:
                item = prev.link.data
                prev.link = prev.link.link  # 이전 노드의 링크를 건너뛰게 연결
                return item
        return None

    def display(self):
        """리스트 전체 원소 출력"""
        node = self.head
        items = []
        while node is not None:
            items.append(node.data)
            node = node.link
        print(f"LinkedList: {items}")


# ==========================================
# 3. 인스턴스 생성 및 사용 예제
# ==========================================
if __name__ == "__main__":
    print("=== [1] 배열 구조 리스트(ArrayList) 테스트 ===")
    arr_list = ArrayList(capacity=10)
    arr_list.insert(0, 10)  # [10]
    arr_list.insert(1, 20)  # [10, 20]
    arr_list.insert(0, 30)  # [30, 10, 20] (맨 앞에 삽입하여 시프팅 발생)
    arr_list.insert(2, 40)  # [30, 10, 40, 20]
    arr_list.display()
    
    print(f"삭제된 원소: {arr_list.delete(1)}")  # 인덱스 1번(10) 삭제
    arr_list.display()
    print("-" * 40)

    print("=== [2] 연결된 구조 리스트(SinglyLinkedList) 테스트 ===")
    link_list = SinglyLinkedList()
    link_list.insert(0, 10)  # [10]
    link_list.insert(1, 20)  # [10, 20]
    link_list.insert(0, 30)  # [30, 10, 20] (시프팅 없이 링크만 연결)
    link_list.insert(2, 40)  # [30, 10, 40, 20]
    link_list.display()
    
    print(f"삭제된 원소: {link_list.delete(1)}")  # 인덱스 1번(10) 삭제
    link_list.display()
