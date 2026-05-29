# ==========================================
# 1. 배열 구조 집합 (ArraySet)
# ==========================================
class ArraySet:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.items = [None] * capacity  # 고정 배열
        self.size = 0

    def contains(self, e):
        """집합 내에 원소 e가 있는지 확인 (중복 방지용)"""
        for i in range(self.size):
            if self.items[i] == e: 
                return True
        return False

    def insert(self, e):
        """중복되지 않고 자리가 있을 때만 맨 뒤에 추가"""
        if not self.contains(e) and self.size < self.capacity:
            self.items[self.size] = e
            self.size += 1

    def delete(self, e):
        """특정 원소를 찾아 삭제 (배열의 마지막 원소를 가져와서 빈자리를 메꿈)"""
        for i in range(self.size):
            if self.items[i] == e:
                self.items[i] = self.items[self.size - 1]  # 맨 뒤 원소로 덮어쓰기
                self.items[self.size - 1] = None
                self.size -= 1
                return True
        return False

    def display(self, msg="ArraySet:"):
        print(msg, self.items[:self.size])

    # --- 집합 연산 기능 추가 ---
    def union(self, setB):
        """합집합 (A ∪ B)"""
        result = ArraySet()
        # 먼저 현재 집합(A)의 모든 원소를 결과에 추가
        for i in range(self.size):
            result.insert(self.items[i])
        # setB의 원소 중 중복되지 않는 것만 추가 (insert 내부에 contains가 있어 자동 중복 제거)
        for i in range(setB.size):
            result.insert(setB.items[i])
        return result

    def intersect(self, setB):
        """교집합 (A ∩ B)"""
        result = ArraySet()
        for i in range(self.size):
            if setB.contains(self.items[i]):
                result.insert(self.items[i])
        return result

    def difference(self, setB):
        """차집합 (A - B)"""
        result = ArraySet()
        for i in range(self.size):
            if not setB.contains(self.items[i]):
                result.insert(self.items[i])
        return result


# ==========================================
# 2. 연결된 구조 집합 (LinkedSet)
# ==========================================
class Node:
    """연결 구조를 위한 노드 클래스"""
    def __init__(self, elem, next=None):
        self.data = elem
        self.link = next

class LinkedSet:
    def __init__(self):
        self.head = None

    def contains(self, e):
        """연결 리스트를 순회하며 원소 e가 있는지 확인"""
        node = self.head
        while node is not None:
            if node.data == e:
                return True
            node = node.link
        return False

    def insert(self, e):
        """중복되지 않을 때만 가장 효율적인 '맨 앞(head)'에 삽입"""
        if not self.contains(e):
            self.head = Node(e, self.head)

    def delete(self, e):
        """특정 원소 e를 찾아 링크 포인터를 변경하여 삭제"""
        if self.head is None:
            return False
        
        # 삭제할 원소가 맨 앞(head)에 있는 경우
        if self.head.data == e:
            self.head = self.head.link
            return True
        
        # 중간이나 뒤에 있는 경우
        prev = self.head
        while prev.link is not None:
            if prev.link.data == e:
                prev.link = prev.link.link  # 건너뛰어 연결
                return True
            prev = prev.link
        return False

    def display(self, msg="LinkedSet:"):
        node = self.head
        items = []
        while node is not None:
            items.append(node.data)
            node = node.link
        print(msg, items)

    # --- 집합 연산 기능 추가 ---
    def union(self, setB):
        result = LinkedSet()
        node = self.head
        while node is not None:
            result.insert(node.data)
            node = node.link
        
        nodeB = setB.head
        while nodeB is not None:
            result.insert(nodeB.data)
            nodeB = nodeB.link
        return result

    def intersect(self, setB):
        result = LinkedSet()
        node = self.head
        while node is not None:
            if setB.contains(node.data):
                result.insert(node.data)
            node = node.link
        return result

    def difference(self, setB):
        result = LinkedSet()
        node = self.head
        while node is not None:
            if not setB.contains(node.data):
                result.insert(node.data)
            node = node.link
        return result


# ==========================================
# 3. 인스턴스 생성 및 집합 연산 예제
# ==========================================
if __name__ == "__main__":
    print("=== [1] 배열 구조 집합(ArraySet) 테스트 ===")
    setA = ArraySet()
    setA.insert(1)
    setA.insert(2)
    setA.insert(3)
    setA.insert(2)  # 중복 테스트 (들어가면 안 됨)
    
    setB = ArraySet()
    setB.insert(3)
    setB.insert(4)
    setB.insert(5)

    setA.display("집합 A:")
    setB.display("집합 B:")
    
    setA.union(setB).display("A ∪ B (합집합):")
    setA.intersect(setB).display("A ∩ B (교집합):")
    setA.difference(setB).display("A - B (차집합):")
    print("-" * 40)

    print("=== [2] 연결된 구조 집합(LinkedSet) 테스트 ===")
    lSetA = LinkedSet()
    lSetA.insert(1)
    lSetA.insert(2)
    lSetA.insert(3)
    lSetA.insert(2)  # 중복 테스트 (들어가면 안 됨)

    lSetB = LinkedSet()
    lSetB.insert(3)
    lSetB.insert(4)
    lSetB.insert(5)

    lSetA.display("집합 A:")
    lSetB.display("집합 B:")

    lSetA.union(lSetB).display("A ∪ B (합집합):")
    lSetA.intersect(lSetB).display("A ∩ B (교집합):")
    lSetA.difference(lSetB).display("A - B (차집합):")
