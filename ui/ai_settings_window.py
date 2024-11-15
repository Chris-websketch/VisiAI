# ui/ai_settings_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFormLayout
from PyQt6.QtCore import Qt
import logging
from utils import settings


class AISettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # 布局和控件
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # 标题标签
        self.title_label = QLabel("AI设置")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
                color: #000000;
            }
        """)
        self.layout.addWidget(self.title_label)

        # 表单布局
        form_layout = QFormLayout()
        self.layout.addLayout(form_layout)

        # 角色性格输入
        self.role_personality_input = QTextEdit()
        self.role_personality_input.setText(self.main_window.role_personality)
        self.role_personality_input.setFixedHeight(100)
        form_layout.addRow("角色性格:", self.role_personality_input)

        # 知识库输入
        self.knowledge_base_input = QTextEdit()
        self.knowledge_base_input.setText(self.main_window.knowledge_base)
        self.knowledge_base_input.setFixedHeight(100)
        form_layout.addRow("知识库:", self.knowledge_base_input)

        # 保存按钮
        self.save_button = QPushButton("保存设置")
        self.save_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px;
                border: none;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QPushButton:pressed {
                background-color: #3E8E41;
            }
        """)
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        # 返回主界面按钮
        self.back_button = QPushButton("返回主界面")
        self.back_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                padding: 10px;
                border: none;
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.back_button.clicked.connect(self.main_window.show_main_widget)
        self.layout.addWidget(self.back_button)

        # 设置背景
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
        """)

    def save_settings(self):
        self.main_window.role_personality = self.role_personality_input.toPlainText()
        self.main_window.knowledge_base = self.knowledge_base_input.toPlainText()
        self.main_window.log("AI设置已保存。")
        logging.info("AI settings saved.")
        # 保存设置
        self.main_window.settings['role_personality'] = self.main_window.role_personality
        self.main_window.settings['knowledge_base'] = self.main_window.knowledge_base
        settings.save_settings(self.main_window.settings)
        self.main_window.show_main_widget()
