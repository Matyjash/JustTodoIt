from dataclasses import replace

from src.ui.theme.theme import DEFAULT_THEME


LAVENDER_THEME_NAME = "Lavender"
LAVENDER_THEME = replace(
    DEFAULT_THEME,
    background_color="#EEEAF7",
    surface_color="#FCFAFF",
    text_color="#392E50",
    lead_color="#7551A8",
    accept_color="#7551A8",
    decline_color="#B53F65",
    neutral_color="#7B708D",
    border_color="#D8CEE8",
)
