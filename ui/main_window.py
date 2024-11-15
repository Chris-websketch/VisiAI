# ui/main_window.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QLabel, QPushButton,
    QTextEdit, QHBoxLayout, QFormLayout, QApplication, QGraphicsOpacityEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QRect, QPoint
from PyQt6.QtGui import QIcon, QColor
import logging
from .ai_settings_window import AISettingsWindow
from .selection_window import SelectionWindow
from .highlight_window import HighlightWindow
from threads.monitoring_thread import MonitoringThread
from utils.helper import perform_mouse_actions
from utils import settings
from PIL import Image
import os
import json
import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置日志记录器
        self.logger = logging.getLogger(__name__)

        self.setWindowTitle("VisiAI")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("dz.ico"))

        # GUI 布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.stacked_widget)

        # 主界面
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.stacked_widget.addWidget(self.main_widget)

        # 标题标签
        self.title_label = QLabel("VisiAI")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #000000;
            }
        """)
        self.title_label_animation()
        self.main_layout.addWidget(self.title_label)

        # 副标题
        self.subtitle_label = QLabel("基于纯视觉的LLM解决方案")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #555555;
            }
        """)
        self.main_layout.addWidget(self.subtitle_label)

        # 添加分割线
        self.add_separator(self.main_layout)

        # 按钮样式
        button_style = """
            QPushButton {
                font-size: 18px;
                padding: 15px;
                border: none;
                background-color: #4A90E2;
                color: white;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2C5C94;
            }
            QPushButton:disabled {
                background-color: #B0B0B0;
            }
        """

        # 按钮布局
        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        # 添加 AI设置 按钮
        self.ai_settings_button = QPushButton("AI设置")
        self.ai_settings_button.setStyleSheet(button_style)
        self.ai_settings_button.clicked.connect(self.show_ai_settings)
        button_layout.addWidget(self.ai_settings_button)

        self.select_chat_button = QPushButton("选择消息区域")
        self.select_chat_button.setStyleSheet(button_style)
        self.select_chat_button.clicked.connect(self.select_chat_area)
        button_layout.addWidget(self.select_chat_button)

        self.select_conversation_button = QPushButton("选择对话区域")
        self.select_conversation_button.setStyleSheet(button_style)
        self.select_conversation_button.clicked.connect(self.select_conversation_area)
        button_layout.addWidget(self.select_conversation_button)

        self.select_input_button = QPushButton("选择输入区域")
        self.select_input_button.setStyleSheet(button_style)
        self.select_input_button.clicked.connect(self.select_input_area)
        button_layout.addWidget(self.select_input_button)

        # 重置区域按钮
        self.reset_areas_button = QPushButton("重置区域")
        self.reset_areas_button.setStyleSheet(button_style)
        self.reset_areas_button.clicked.connect(self.reset_areas)
        self.main_layout.addWidget(self.reset_areas_button)

        # 添加分割线
        self.add_separator(self.main_layout)

        # 监控控制按钮
        self.control_layout = QHBoxLayout()
        self.main_layout.addLayout(self.control_layout)

        self.start_button = QPushButton("开始监控")
        self.start_button.setStyleSheet(button_style)
        self.start_button.clicked.connect(self.start_monitoring_thread)
        self.control_layout.addWidget(self.start_button)

        self.pause_button = QPushButton("暂停")
        self.pause_button.setStyleSheet(button_style)
        self.pause_button.clicked.connect(self.pause_monitoring)
        self.pause_button.setEnabled(False)
        self.control_layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("继续")
        self.resume_button.setStyleSheet(button_style)
        self.resume_button.clicked.connect(self.resume_monitoring)
        self.resume_button.setEnabled(False)
        self.control_layout.addWidget(self.resume_button)

        self.stop_button = QPushButton("停止监控")
        self.stop_button.setStyleSheet(button_style)
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        self.control_layout.addWidget(self.stop_button)

        # 添加分割线
        self.add_separator(self.main_layout)

        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-size: 14px;
                padding: 10px;
                border: 1px solid #CCCCCC;
                background-color: #E0E0E0;
            }
        """)
        self.main_layout.addWidget(self.log_text)

        # 初始化区域
        self.chat_area = None
        self.conversation_area = None
        self.input_area = None
        # 初始化目标图像
        self.target_images = []
        target_image_folder = "opencv"
        for filename in os.listdir(target_image_folder):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(target_image_folder, filename)
                image = Image.open(image_path)
                self.target_images.append(image)
        self.log(f"已加载初始资源")
        logging.info("Initial resources loaded.")

        # 高亮窗口
        self.highlight_window = HighlightWindow()
        self.highlight_areas = []

        # Image upload API token and URL
        self.upload_token = "2803fc0b27c12aea3ee401f60d67e17c"  # Replace with your actual token
        self.upload_url = "https://imgbad.xmduzhong.com/api/index.php"  # Replace with your actual upload URL

        self.monitoring_thread = None

        # AI 设置变量
        self.role_personality = ""
        self.knowledge_base = ""

        # 创建 AI 设置界面
        self.create_ai_settings_widget()

        # 加载本地保存的设置
        self.load_settings()  # 新增：加载设置

        # 设置高 DPI 感知
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

        # 设置主界面背景
        self.set_main_background()

    def set_main_background(self):
        # 设置背景图片或颜色
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
        """)

    def title_label_animation(self):
        # 添加标题淡入动画
        self.title_animation = QPropertyAnimation(self.title_label, b"opacity")
        self.title_animation.setDuration(2000)
        self.title_animation.setStartValue(0)
        self.title_animation.setEndValue(1)
        self.title_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        opacity_effect = QGraphicsOpacityEffect()
        self.title_label.setGraphicsEffect(opacity_effect)
        self.title_label.opacity_effect = opacity_effect  # 保持对效果的引用
        self.title_animation.start()

    def add_separator(self, layout):
        # 添加分割线
        separator = QLabel()
        separator.setFixedHeight(2)
        separator.setStyleSheet("background-color: #555555;")
        layout.addWidget(separator)

    def create_ai_settings_widget(self):
        self.ai_settings_widget = QWidget()
        self.ai_settings_layout = QVBoxLayout(self.ai_settings_widget)
        self.stacked_widget.addWidget(self.ai_settings_widget)

        # 标题标签
        self.ai_settings_title = QLabel("AI设置")
        self.ai_settings_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ai_settings_title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
                color: #000000;
            }
        """)
        self.ai_settings_layout.addWidget(self.ai_settings_title)

        # 表单布局
        form_layout = QFormLayout()
        self.ai_settings_layout.addLayout(form_layout)

        # 角色性格输入
        self.role_personality_input = QTextEdit()
        self.role_personality_input.setText(self.role_personality)
        self.role_personality_input.setFixedHeight(100)
        form_layout.addRow("角色性格:", self.role_personality_input)

        # 知识库输入
        self.knowledge_base_input = QTextEdit()
        self.knowledge_base_input.setText(self.knowledge_base)
        self.knowledge_base_input.setFixedHeight(100)
        form_layout.addRow("知识库:", self.knowledge_base_input)

        # 保存按钮
        self.save_ai_settings_button = QPushButton("保存设置")
        self.save_ai_settings_button.setStyleSheet("""
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
        self.save_ai_settings_button.clicked.connect(self.save_ai_settings)
        self.ai_settings_layout.addWidget(self.save_ai_settings_button)

        # 返回主界面按钮
        self.back_to_main_button = QPushButton("返回主界面")
        self.back_to_main_button.setStyleSheet("""
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
        self.back_to_main_button.clicked.connect(self.show_main_widget)
        self.ai_settings_layout.addWidget(self.back_to_main_button)

        # 设置 AI 设置界面背景
        self.ai_settings_widget.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
            }
        """)

    def show_ai_settings(self):
        # 添加界面切换动画
        self.stacked_widget.setCurrentWidget(self.ai_settings_widget)
        self.fade_in_animation(self.ai_settings_widget)

    def show_main_widget(self):
        # 添加界面切换动画
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.fade_in_animation(self.main_widget)

    def fade_in_animation(self, widget):
        self.fade_animation = QPropertyAnimation(widget, b"opacity")
        self.fade_animation.setDuration(500)
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        widget.opacity_effect = opacity_effect  # 保持对效果的引用
        self.fade_animation.start()

    def save_ai_settings(self):
        self.role_personality = self.role_personality_input.toPlainText()
        self.knowledge_base = self.knowledge_base_input.toPlainText()
        self.log("AI设置已保存。")
        logging.info("AI settings saved.")
        self.show_main_widget()
        self.save_settings()  # 新增：保存设置

    def load_settings(self):
        """加载本地保存的设置"""
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
                self.role_personality = settings_data.get('role_personality', self.role_personality)
                self.knowledge_base = settings_data.get('knowledge_base', self.knowledge_base)
                self.role_personality_input.setText(self.role_personality)
                self.knowledge_base_input.setText(self.knowledge_base)
                self.log("已加载本地配置。")
                self.log("程序准备完毕")
                logging.info("Local settings loaded.")
        except FileNotFoundError:
            self.log("未找到本地配置文件，使用默认设置。")
            logging.warning("Settings file not found; using default settings.")
        except Exception as e:
            self.log("加载配置时遇到问题，使用默认设置。")
            logging.exception("Exception while loading settings.")

    def save_settings(self):
        """保存设置到本地 JSON 文件"""
        settings_data = {
            'role_personality': self.role_personality,
            'knowledge_base': self.knowledge_base
        }
        try:
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=4)
            self.log("配置已保存。")
            logging.info("Settings saved to file.")
        except Exception as e:
            self.log("保存配置时遇到问题。")
            logging.exception("Exception while saving settings.")

    def log(self, message, level=logging.INFO):
        """显示日志信息"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"[{timestamp}] {message}"
        self.log_text.append(full_message)
        print(full_message)
        logging.log(level, message)

    # 以下是缺失的方法，需要补充到 MainWindow 类中

    def select_chat_area(self):
        self.log("请拖动鼠标选择消息区域...")
        logging.info("Selecting chat area.")
        self.selection_window = SelectionWindow("选择消息区域")
        self.selection_window.area_selected.connect(self.set_chat_area)
        self.selection_window.show()

    def set_chat_area(self, rect):
        self.chat_area = (rect.x(), rect.y(), rect.width(), rect.height())
        self.subtitle_label.setText("消息区域已选择")
        self.log("消息区域已成功选择。")
        logging.info(f"Chat area set to: {self.chat_area}")

        # 更新高亮区域
        self.highlight_areas = [area for area in self.highlight_areas if area['label'] != '消息区域']
        self.highlight_areas.append({
            'rect': self.chat_area,
            'color': QColor(0, 255, 0, 50),  # 半透明绿色
            'label': '消息区域'
        })
        self.highlight_window.update_areas(self.highlight_areas)
        self.highlight_window.show()

    def select_conversation_area(self):
        self.log("请拖动鼠标选择会话区域...")
        logging.info("Selecting conversation area.")
        self.selection_window = SelectionWindow("选择会话区域")
        self.selection_window.area_selected.connect(self.set_conversation_area)
        self.selection_window.show()

    def set_conversation_area(self, rect):
        self.conversation_area = (rect.x(), rect.y(), rect.width(), rect.height())
        self.subtitle_label.setText("会话区域已选择")
        self.log("会话区域已成功选择。")
        logging.info(f"Conversation area set to: {self.conversation_area}")

        # 更新高亮区域
        self.highlight_areas = [area for area in self.highlight_areas if area['label'] != '会话区域']
        self.highlight_areas.append({
            'rect': self.conversation_area,
            'color': QColor(255, 0, 0, 50),  # 半透明红色
            'label': '会话区域'
        })
        self.highlight_window.update_areas(self.highlight_areas)
        self.highlight_window.show()

    def select_input_area(self):
        self.log("请拖动鼠标选择输入框区域...")
        logging.info("Selecting input area.")
        self.selection_window = SelectionWindow("选择输入框区域")
        self.selection_window.area_selected.connect(self.set_input_area)
        self.selection_window.show()

    def set_input_area(self, rect):
        self.input_area = (rect.x(), rect.y(), rect.width(), rect.height())
        self.subtitle_label.setText("输入框区域已选择")
        self.log("输入框区域已成功选择。")
        logging.info(f"Input area set to: {self.input_area}")

        # 更新高亮区域
        self.highlight_areas = [area for area in self.highlight_areas if area['label'] != '输入框区域']
        self.highlight_areas.append({
            'rect': self.input_area,
            'color': QColor(0, 0, 255, 50),  # 半透明蓝色
            'label': '输入框区域'
        })
        self.highlight_window.update_areas(self.highlight_areas)
        self.highlight_window.show()

    def reset_areas(self):
        self.chat_area = None
        self.conversation_area = None
        self.input_area = None
        self.highlight_areas = []
        self.highlight_window.update_areas(self.highlight_areas)
        self.subtitle_label.setText("所有区域已重置，请重新选择。")
        self.log("已重置所有区域，请重新选择。")
        logging.info("All areas have been reset.")

    def start_monitoring_thread(self):
        if not self.chat_area or not self.conversation_area or not self.input_area:
            self.subtitle_label.setText("请先选择所有区域")
            self.log("请先选择所有需要的区域。")
            logging.warning("Attempted to start monitoring without all areas selected.")
            return

        self.monitoring_thread = MonitoringThread(self)
        self.monitoring_thread.log_signal.connect(self.log)
        self.monitoring_thread.update_label_signal.connect(self.subtitle_label.setText)
        # 连接其他信号...
        # 请确保在 MonitoringThread 中定义了必要的信号，并在这里进行连接

        self.monitoring_thread.start()
        self.start_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.subtitle_label.setText("正在监控中...")
        self.log("自动回复功能已启动。")
        logging.info("Monitoring thread started.")

    def pause_monitoring(self):
        if self.monitoring_thread and self.monitoring_thread.isRunning():
            self.monitoring_thread.pause()
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(True)
            self.subtitle_label.setText("监控已暂停。")

    def resume_monitoring(self):
        if self.monitoring_thread and self.monitoring_thread.isRunning():
            self.monitoring_thread.resume()
            self.pause_button.setEnabled(True)
            self.resume_button.setEnabled(False)
            self.subtitle_label.setText("监控已继续。")

    def stop_monitoring(self):
        if self.monitoring_thread and self.monitoring_thread.isRunning():
            self.monitoring_thread.stop()
            self.monitoring_thread.wait()
            self.start_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.subtitle_label.setText("监控已停止。")
            self.log("自动回复功能已停止。")
            logging.info("Monitoring thread stopped.")
