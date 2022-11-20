from PyQt6.QtGui import QFont

# Font settings
FONT_NAME: str = "Arial"
FONT: QFont = QFont(FONT_NAME)

SMALL_FONT = QFont(FONT_NAME, pointSize=5)
LARGE_FONT = QFont(FONT_NAME, pointSize=11)

BOLD_FONT: QFont = QFont(FONT_NAME)
BOLD_FONT.setBold(True)
LARGE_BOLD_FONT = QFont(FONT_NAME, pointSize=11)
LARGE_BOLD_FONT.setBold(True)

ITALIC_FONT: QFont = QFont(FONT_NAME)
ITALIC_FONT.setItalic(True)
