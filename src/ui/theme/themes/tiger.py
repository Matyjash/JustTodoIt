from dataclasses import replace

from src.ui.theme.theme import DEFAULT_THEME


TIGER_THEME_NAME = "Tiger"
TIGER_THEME = replace(
    DEFAULT_THEME,
    background_color="#000000",
    surface_color="#1A1A1A",
    text_color="#F5F5F5",
    lead_color="#FFA500",
    accept_color="#FFA500",
    decline_color="#f44336",
    neutral_color="#616161",
    border_color="#424242",
)
