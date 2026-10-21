from dataclasses import dataclass, replace


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
    title_padding: str = "10px"

    input_padding: str = "8px"
    input_border_radius: str = "4px"

    add_btn_padding: str = "8px 15px"

    list_border_radius: str = "4px"
    list_item_padding: str = "10px"
    list_item_font_name: str = "Arial"
    list_item_font_size: int = 10

    delete_btn_padding: str = "8px 15px"

    clear_btn_padding: str = "8px 15px"

    edit_btn_padding: str = "6px"

    save_btn_padding: str = "8px 15px"

    task_status_square_size: int = 20
    task_status_square_padding: str = "4px"


DEFAULT_THEME = Theme()
DEFAULT_THEME_NAME = "Default"

BLUE_THEME_NAME = "Blue"
BLUE_THEME = replace(
    DEFAULT_THEME,
    background_color="#E8EAF6",
    lead_color="#3F51B5",
    accept_color="#3F51B5",
)

TIGER_THEME_NAME = "Tiger"
TIGER_THEME = replace(
    DEFAULT_THEME,
    background_color="#000000",
    surface_color="#1A1A1A",
    text_color="#F5F5F5",
    lead_color="#FFA500",
    accept_color="#FFA500",
    decline_color="#E65100",
    neutral_color="#616161",
    border_color="#424242",
)

THEMES = {
    DEFAULT_THEME_NAME: DEFAULT_THEME,
    BLUE_THEME_NAME: BLUE_THEME,
    TIGER_THEME_NAME: TIGER_THEME,
}
