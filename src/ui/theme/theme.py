from dataclasses import dataclass


@dataclass
class Theme:
    background_color: str = "#f0f0f0"
    surface_color: str = "white"
    text_color: str = "black"
    button_text_color: str = "white"
    lead_color: str = "#4CAF50"
    accept_color: str = "#4CAF50"
    decline_color: str = "#f44336"
    neutral_color: str = "#9e9e9e"
    border_color: str = "#EBEAEA"

    title_font_name: str = "Arial"
    title_font_size: int = 14

    input_padding: str = "8px"
    input_border_radius: str = "4px"

    add_btn_padding: str = "8px 15px"

    list_border_radius: str = "4px"
    list_item_font_name: str = "Arial"
    list_item_font_size: int = 10

    task_row_button_size: int = 20
    task_row_button_padding: int = 4
    task_row_button_border_radius: int = 2

    delete_btn_padding: str = "8px 15px"

    save_btn_padding: str = "8px 15px"


DEFAULT_THEME = Theme()
DEFAULT_THEME_NAME = "Default"
