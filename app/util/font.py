from PyQt6.QtGui import QFont

FONT_NAME: str = "Arial"
FONT: QFont = QFont(FONT_NAME)

SMALL_FONT = QFont(FONT_NAME, pointSize=5)

BOLD_FONT: QFont = QFont(FONT_NAME)
BOLD_FONT.setBold(True)

ITALIC_FONT: QFont = QFont(FONT_NAME)
ITALIC_FONT.setItalic(True)
