import flet as ft

# ==========================================
# 1. 자료구조 Stack 구조 (유지)
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

    def peek(self):
        if not self.isEmpty(): 
            return self.array[self.top]
        return None


# ==========================================
# 2. 중위표기식 -> 후위표기식 변환 알고리즘 (유지)
# ==========================================
def precedence(op):
    if op in ['(', ')']: return 0
    if op in ['+', '-']: return 1
    if op in ['*', '/']: return 2
    return -1

def infix_to_postfix(expr_list):
    s = Stack()
    postfix = []
    
    for term in expr_list:
        if term == '(':
            s.push(term)
        elif term == ')':
            while not s.isEmpty():
                op = s.pop()
                if op == '(': break
                postfix.append(op)
        elif term in ['+', '-', '*', '/']:
            while not s.isEmpty() and precedence(s.peek()) >= precedence(term):
                postfix.append(s.pop())
            s.push(term)
        else:
            postfix.append(term)
            
    while not s.isEmpty():
        postfix.append(s.pop())
        
    return postfix


# ==========================================
# 3. 후위표기식 계산 로직 (유지)
# ==========================================
def eval_postfix(postfix_list):
    s = Stack()
    
    for char in postfix_list:
        if char.replace('.', '', 1).isdigit() or (char.startswith('-') and char[1:].replace('.', '', 1).isdigit()):
            s.push(float(char))
        else:
            n2 = s.pop()
            n1 = s.pop()
            if n1 is None or n2 is None:
                return "수식 오류"
            if char == '+': s.push(n1 + n2)
            elif char == '-': s.push(n1 - n2)
            elif char == '*': s.push(n1 * n2)
            elif char == '/': 
                if n2 == 0: return "0으로 나눌 수 없음"
                s.push(n1 / n2)
                
    final_res = s.pop()
    if isinstance(final_res, float) and final_res.is_integer():
        return int(final_res)
    return final_res


# ==========================================
# 4. 최신 Flet 완전 무결격 뷰 레이아웃 구현
# ==========================================
def main(page: ft.Page):
    page.title = "수식 계산기"
    page.window.width = 450
    page.window.height = 600
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK

    current_tokens = []

    # 입출력 모니터 창
    display_input = ft.TextField(
        value="",
        text_align=ft.TextAlign.RIGHT,
        text_size=28,
        read_only=True,
        border_radius=10,
        bgcolor=ft.Colors.BLACK26,
        color=ft.Colors.WHITE
    )
    
    postfix_text = ft.Text(value="후위 표현식: ", color=ft.Colors.BLUE_200, size=14)
    status_text = ft.Text(value="스택 수식 스케줄러 대기 중", color=ft.Colors.GREY_500, size=13)

    def update_screen(display_val, postfix_val=None, status_val=None, is_error=False):
        display_input.value = display_val
        if postfix_val is not None:
            postfix_text.value = f"후위 표현식: {postfix_val}"
        if status_val is not None:
            status_text.value = status_val
            status_text.color = ft.Colors.RED_400 if is_error else ft.Colors.GREEN_400
            
        display_input.update()
        postfix_text.update()
        status_text.update()

    # 클릭 이벤트 헨들러
    def button_clicked(e):
        # 최신 스펙에서는 데이터 속성(data)을 추적하는 구조가 가장 안전합니다.
        data = e.control.data  
        
        if data == "C":
            current_tokens.clear()
            update_screen("", "", "초기화 완료")
        elif data == "⌫":
            if current_tokens:
                current_tokens.pop()
            update_screen(" ".join(current_tokens))
        elif data == "=":
            if not current_tokens:
                return
            try:
                postfix_res = infix_to_postfix(current_tokens)
                postfix_str = " ".join(postfix_res)
                result = eval_postfix(postfix_res)
                
                if "오류" in str(result) or "나눌" in str(result):
                    update_screen("Error", postfix_str, result, is_error=True)
                else:
                    update_screen(str(result), postfix_str, "계산 성공")
                    current_tokens.clear()
                    current_tokens.append(str(result))
            except Exception as ex:
                update_screen("Error", "변환 실패", f"예외 발생: {str(ex)}", is_error=True)
        else:
            current_tokens.append(data)
            update_screen(" ".join(current_tokens))

    # [에러 해결] text='...' 인수를 완전히 지우고, content=ft.Text('...') 구조로 표준 캡슐화 완료
    def btn(text_val, bg_color=None):
        return ft.ElevatedButton(
            content=ft.Text(value=text_val, color=ft.Colors.WHITE, size=16),
            data=text_val, # 이벤트 구분을 위해 메타데이터 슬롯에 수식 기호 바인딩
            on_click=button_clicked,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=bg_color if bg_color else ft.Colors.SURFACE_CONTAINER_HIGH,
                padding=15
            ),
            expand=True
        )

    # 레이아웃 구성
    calc_layout = ft.Column([
        ft.Text("수식 계산기 (Stack & Flet)", size=20, weight=ft.FontWeight.BOLD),
        display_input,
        postfix_text,
        status_text,
        ft.Divider(),
        
        ft.Row([
            btn("(", ft.Colors.BLUE_GREY_800),
            btn(")", ft.Colors.BLUE_GREY_800),
            btn("⌫", ft.Colors.RED_900),
            btn("C", ft.Colors.RED_900),
        ], spacing=8),
        
        ft.Row([
            btn("7"), btn("8"), btn("9"),
            btn("/", ft.Colors.ORANGE_900),
        ], spacing=8),
        
        ft.Row([
            btn("4"), btn("5"), btn("6"),
            btn("*", ft.Colors.ORANGE_900),
        ], spacing=8),
        
        ft.Row([
            btn("1"), btn("2"), btn("3"),
            btn("-", ft.Colors.ORANGE_900),
        ], spacing=8),
        
        ft.Row([
            btn("0"), 
            btn("."), 
            btn("=", ft.Colors.BLUE_900),
            btn("+", ft.Colors.ORANGE_900),
        ], spacing=8),
    ], spacing=12, expand=True)

    page.add(calc_layout)

if __name__ == "__main__":
    ft.app(target=main)
