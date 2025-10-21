from app.models.display_panel import DisplayPanel


class Floor:
    def __init__(self, floor_number: int) -> None:
        self.floor_number = floor_number
        self.display_panel = DisplayPanel(f"Floor {floor_number} Display")

    def get_floor_number(self) -> int:
        return self.floor_number

    def get_display_panel(self) -> DisplayPanel:
        return self.display_panel

    def get_display_panel_content(self) -> str:
        return self.display_panel.get_content()

    def update_display_panel_content(self, updated_content: str) -> None:
        self.display_panel.update_content(updated_content)
