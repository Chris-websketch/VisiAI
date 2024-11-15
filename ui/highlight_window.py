# ui/highlight_window.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor, QFont

class HighlightWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("区域高亮")
        # 设置窗口标志，使窗口对输入事件透明
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.full_screen_rect = self.screen().availableGeometry()
        self.setGeometry(self.full_screen_rect)
        self.selected_areas = []
        self.showFullScreen()

    def update_areas(self, areas):
        self.selected_areas = areas
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        for area in self.selected_areas:
            color = area['color']
            rect = area['rect']
            label = area['label']
            brush = QBrush(color)
            painter.fillRect(QRect(*rect), brush)
            # 绘制标签
            painter.setPen(QPen(QColor(255, 255, 255)))
            font = QFont()
            font.setPointSize(16)
            painter.setFont(font)
            painter.drawText(QRect(*rect), Qt.AlignmentFlag.AlignCenter, label)
