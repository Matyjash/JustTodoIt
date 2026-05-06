from dataclasses import dataclass


@dataclass
class Style:
    window_background: str = "#f0f0f0"

    title_font_name: str = "Arial"
    title_font_size: int = 14
    title_bg_color: str = "#4CAF50"
    title_text_color: str = "white"
    title_padding: str = "10px"

    input_padding: str = "8px"
    input_border: str = "1px solid #ddd"
    input_border_radius: str = "4px"

    add_btn_bg_color: str = "#4CAF50"
    add_btn_text_color: str = "white"
    add_btn_padding: str = "8px 15px"
    add_btn_hover_color: str = "#45a049"

    list_border: str = "1px solid #ddd"
    list_border_radius: str = "4px"
    list_bg_color: str = "white"
    list_item_padding: str = "10px"
    list_item_border_bottom: str = "1px solid #eee"
    list_item_selected_bg: str = "#e8f5e9"
    list_item_font_name: str = "Arial"
    list_item_font_size: int = 10

    delete_btn_bg_color: str = "#f44336"
    delete_btn_text_color: str = "white"
    delete_btn_padding: str = "8px 15px"
    delete_btn_hover_color: str = "#da190b"

    clear_btn_bg_color: str = "#ff9800"
    clear_btn_text_color: str = "white"
    clear_btn_padding: str = "8px 15px"
    clear_btn_hover_color: str = "#e68900"


DEFAULT_STYLE = Style()
