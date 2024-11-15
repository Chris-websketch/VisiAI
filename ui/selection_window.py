# ui/selection_window.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, Qt, QRect, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont

class SelectionWindow(QWidget):
    area_selected = pyqtSignal(QRect)

    def __init__(self, label_text):
        super().__init__()
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.setWindowTitle("选择区域")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.3)
        self.full_screen_rect = self.screen().availableGeometry()
        self.setGeometry(self.full_screen_rect)
        self.setStyleSheet("background-color: rgba(0,0,0,0.5);")
        self.showFullScreen()
        self.is_selecting = False
        self.label_text = label_text

    def mousePressEvent(self, event):
        self.is_selecting = True
        self.start_point = event.pos()
        self.end_point = self.start_point
        self.update()

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        self.is_selecting = False
        self.end_point = event.pos()
        self.update()
        rect = QRect(self.start_point, self.end_point).normalized()
        self.area_selected.emit(rect)
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        # 绘制半透明覆盖层
        brush = QBrush(QColor(0, 0, 0, 100))
        painter.fillRect(self.rect(), brush)

        if self.is_selecting:
            rect = QRect(self.start_point, self.end_point)
            painter.drawRect(rect)

        # 绘制标签
        painter.setPen(QPen(QColor(255, 255, 255)))
        font = QFont()
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter, self.label_text)
