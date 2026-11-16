from dataclasses import replace

from src.ui.theme.theme import DEFAULT_THEME


MIDNIGHT_THEME_NAME = "Midnight"
MIDNIGHT_THEME = replace(
    DEFAULT_THEME,
    background_color="#101B2B",
    surface_color="#19283C",
    text_color="#E6EFF9",
    lead_color="#246A88",
    accept_color="#246A88",
    decline_color="#B54459",
    neutral_color="#50637D",
    border_color="#35475F",
)
