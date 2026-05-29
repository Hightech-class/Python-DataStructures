import flet as ft
import os

# ==========================================
# 1. 자료구조 ArrayList (안정성 보완)
# ==========================================
class ArrayList:
    def __init__(self):
        self.items = []
        self.size_count = 0

    def insert(self, pos, value):
        if pos < 0: pos = 0
        if pos > self.size_count: pos = self.size_count
        self.items.insert(pos, value)
        self.size_count += 1

    def delete(self, pos):
        if 0 <= pos < self.size_count:
            item = self.items.pop(pos)
            self.size_count -= 1
            return item
        return None

    def replace(self, pos, value):
        if 0 <= pos < self.size_count:
            self.items[pos] = value
            return True
        return False

    def clear(self):
        self.items = []
        self.size_count = 0


# ==========================================
# 2. 최신 규격 방어형 GUI 구현
# ==========================================
def main(page: ft.Page):
    # [방어 코드 1] 최신 타이틀 및 가상 캔버스 크기 지정
    page.title = "라인 편집기"
    page.theme_mode = ft.ThemeMode.DARK
    
    # [방어 코드 2] 최신 Flet에서는 윈도우 크기 변경 시 비동기 업데이트 컨텍스트를 동기화해야 합니다.
    page.window.width = 700
    page.window.height = 650
    page.window.resizable = False # 크기 조절로 인한 UI 깨짐 원천 차단

    lines = ArrayList()
    FILE_NAME = "editor_output.txt"

    # [방어 코드 3] 인풋 필드의 입력 데이터 누락 및 널 포인터 방어 설정
    pos_input = ft.TextField(
        label="행 번호", 
        width=100, 
        hint_text="번호", 
        keyboard_type=ft.KeyboardType.NUMBER,
        value="" # 초기화 에러 방지
    )
    text_input = ft.TextField(
        label="내용", 
        expand=True, 
        hint_text="텍스트를 입력하세요.",
        value="" # 초기화 에러 방지
    )
    
    # [방어 코드 4] 최신 리스트뷰는 내부 스크롤 이벤트와 컨테이너 확장이 충돌할 수 있으므로
    # auto_scroll 혹은 정적 높이 확장을 명시하는 것이 안전합니다.
    line_list_view = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=False)
    status_text = ft.Text(value="시스템 준비 완료", color=ft.Colors.GREEN_400, size=14)

    def update_editor_display():
        line_list_view.controls.clear()
        if lines.size_count == 0:
            line_list_view.controls.append(
                ft.Text("입력된 내용이 없습니다. 아래 메뉴를 통해 텍스트를 삽입해 보세요.", color=ft.Colors.GREY_500, italic=True)
            )
        else:
            for i in range(lines.size_count):
                line_list_view.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"[{i:02d}]", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300, width=50),
                            ft.Text(lines.items[i], size=16, expand=True)
                        ]),
                        padding=8,
                        # [방어 코드 5] 완전 제거된 SURFACE_VARIANT 대신 표준 Material 3 테마 컨테이너 색상 적용
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, 
                        border_radius=5
                    )
                )
        line_list_view.update()

    # 이벤트 핸들러
    def on_insert_click(e):
        try:
            pos = int(pos_input.value) if pos_input.value.strip() else lines.size_count
            val = text_input.value if text_input.value else ""
            lines.insert(pos, val)
            
            status_text.value = f"{pos}번 행에 삽입되었습니다."
            status_text.color = ft.Colors.GREEN_400
            text_input.value = ""
            
            status_text.update()
            text_input.update()
            update_editor_display()
        except ValueError:
            status_text.value = "에러: 행 번호에는 숫자만 입력할 수 있습니다."
            status_text.color = ft.Colors.RED_400
            status_text.update()

    def on_delete_click(e):
        try:
            if not pos_input.value.strip():
                status_text.value = "에러: 삭제할 행 번호를 지정해야 합니다."
                status_text.color = ft.Colors.RED_400
                status_text.update()
                return
            pos = int(pos_input.value)
            deleted_item = lines.delete(pos)
            if deleted_item is not None:
                status_text.value = f"{pos}번 행이 삭제되었습니다."
                status_text.color = ft.Colors.ORANGE_400
                status_text.update()
                update_editor_display()
            else:
                status_text.value = "에러: 해당 행 번호가 존재하지 않습니다."
                status_text.color = ft.Colors.RED_400
                status_text.update()
        except ValueError:
            status_text.value = "에러: 행 번호에는 숫자만 입력할 수 있습니다."
            status_text.color = ft.Colors.RED_400
            status_text.update()

    def on_replace_click(e):
        try:
            if not pos_input.value.strip():
                status_text.value = "에러: 변경할 행 번호를 지정해야 합니다."
                status_text.color = ft.Colors.RED_400
                status_text.update()
                return
            pos = int(pos_input.value)
            val = text_input.value if text_input.value else ""
            if lines.replace(pos, val):
                status_text.value = f"{pos}번 행이 변경되었습니다."
                status_text.color = ft.Colors.GREEN_400
                text_input.value = ""
                status_text.update()
                text_input.update()
                update_editor_display()
            else:
                status_text.value = "에러: 해당 행 번호가 존재하지 않습니다."
                status_text.color = ft.Colors.RED_400
                status_text.update()
        except ValueError:
            status_text.value = "에러: 행 번호에는 숫자만 입력할 수 있습니다."
            status_text.color = ft.Colors.RED_400
            status_text.update()

    def on_save_click(e):
        try:
            with open(FILE_NAME, "w", encoding="utf-8") as f:
                for item in lines.items:
                    f.write(item + "\n")
            status_text.value = f"'{FILE_NAME}'에 저장되었습니다."
            status_text.color = ft.Colors.BLUE_200
        except Exception as ex:
            status_text.value = f"파일 저장 실패: {str(ex)}"
            status_text.color = ft.Colors.RED_400
        status_text.update()

    def on_load_click(e):
        if not os.path.exists(FILE_NAME):
            status_text.value = f"에러: 불러올 '{FILE_NAME}' 파일이 없습니다."
            status_text.color = ft.Colors.RED_400
            status_text.update()
            return
        try:
            lines.clear()
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                for line in f:
                    lines.insert(lines.size_count, line.strip())
            status_text.value = f"'{FILE_NAME}'에서 데이터를 읽어왔습니다."
            status_text.color = ft.Colors.BLUE_200
            status_text.update()
            update_editor_display()
        except Exception as ex:
            status_text.value = f"파일 읽기 실패: {str(ex)}"
            status_text.color = ft.Colors.RED_400
            status_text.update()

    # [방어 코드 6] 컴포넌트들을 담는 최상위 스택 레이아웃의 무한 확장 에러 방지용 가이드 구성
    main_layout = ft.Column([
        ft.Text("라인 편집기", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        
        ft.Text("현재 문서 내용", size=14, color=ft.Colors.BLUE_200),
        ft.Container(
            content=line_list_view,
            border=ft.border.all(1, ft.Colors.GREY_700),
            border_radius=10,
            height=300,
            bgcolor=ft.Colors.BLACK12
        ),
        
        ft.Row([pos_input, text_input], spacing=10),
        
        ft.Row([
            ft.ElevatedButton("i: 삽입", icon="add", on_click=on_insert_click, bgcolor=ft.Colors.BLUE_900),
            ft.ElevatedButton("d: 삭제", icon="delete", on_click=on_delete_click, bgcolor=ft.Colors.RED_900),
            ft.ElevatedButton("r: 변경", icon="edit", on_click=on_replace_click, bgcolor=ft.Colors.GREEN_900),
            ft.ElevatedButton("l: 로드", icon="file_open", on_click=on_load_click),
            ft.ElevatedButton("s: 저장", icon="save", on_click=on_save_click),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        
        ft.Divider(),
        ft.Row([
            ft.Text("상태: ", weight=ft.FontWeight.BOLD),
            status_text
        ])
    ], expand=True, spacing=15)

    # 페이지에 레이아웃 추가 후 마지막에 딱 한 번만 page.update() 호출하여 안전하게 뷰 초기화
    page.add(main_layout)
    update_editor_display()
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
