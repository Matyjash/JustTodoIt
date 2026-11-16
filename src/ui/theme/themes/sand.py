from dataclasses import replace

from src.ui.theme.theme import DEFAULT_THEME


SAND_THEME_NAME = "Sand"
SAND_THEME = replace(
    DEFAULT_THEME,
    background_color="#F2E8DA",
    surface_color="#FFFAF2",
    text_color="#49392D",
    lead_color="#9B542F",
    accept_color="#9B542F",
    decline_color="#AD3F38",
    neutral_color="#82715F",
    border_color="#DDCCB5",
)
