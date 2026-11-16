from dataclasses import replace

from src.ui.theme.theme import DEFAULT_THEME


BLUE_THEME_NAME = "Blue"
BLUE_THEME = replace(
    DEFAULT_THEME,
    background_color="#E8EAF6",
    lead_color="#3F51B5",
    accept_color="#3F51B5",
)
