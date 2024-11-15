# main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import setup_logging
from PyQt6.QtCore import Qt

if __name__ == "__main__":
    setup_logging()

    # 设置高 DPI 感知
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
