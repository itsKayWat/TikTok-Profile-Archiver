class Theme:
    # Colors
    DARK_BG = "#1A1B1E"
    DARKER_BG = "#141517"
    NEON_GREEN = "#4ADE80"
    HOVER_GREEN = "#22C55E"
    TEXT_COLOR = "#E2E8F0"
    SECONDARY_TEXT = "#94A3B8"
    INPUT_BG = "#24262B"
    BORDER_COLOR = "#2D3139"

    # Styles
    input_style = f"""
        QLineEdit {{
            background-color: {INPUT_BG};
            color: {TEXT_COLOR};
            border: 1px solid {BORDER_COLOR};
            padding: 8px;
            border-radius: 4px;
        }}
        QLineEdit:hover {{
            border-color: {NEON_GREEN};
        }}
    """

    primary_button_style = f"""
        QPushButton {{
            background-color: {NEON_GREEN};
            color: {DARK_BG};
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {HOVER_GREEN};
        }}
    """

    secondary_button_style = f"""
        QPushButton {{
            background-color: transparent;
            color: {NEON_GREEN};
            border: 1px solid {NEON_GREEN};
            padding: 8px 16px;
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: {NEON_GREEN};
            color: {DARK_BG};
        }}
    """ 