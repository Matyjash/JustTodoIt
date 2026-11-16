from dataclasses import replace

from src.ui.theme.theme import DEFAULT_THEME


FOREST_THEME_NAME = "Forest"
FOREST_THEME = replace(
    DEFAULT_THEME,
    background_color="#E8EFE8",
    surface_color="#F8FBF6",
    text_color="#243D30",
    lead_color="#2D6448",
    accept_color="#2D6448",
    decline_color="#B54740",
    neutral_color="#65796B",
    border_color="#C7D6C8",
)
