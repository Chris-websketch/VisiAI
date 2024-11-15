# threads/monitoring_thread.py
from PyQt6.QtCore import QThread, pyqtSignal, QRect, QEventLoop
import threading
import random
import logging
import pyautogui
from PIL import Image
from utils.image_utils import upload_image
from utils.ai_api import upload_and_get_reply
import time

class MonitoringThread(QThread):
    # 定义信号
    log_signal = pyqtSignal(str)
    update_label_signal = pyqtSignal(str)
    show_mouse_position_signal = pyqtSignal(int, int)
    input_reply_signal = pyqtSignal(str)
    click_position_signal = pyqtSignal(int, int)  # 请求在指定位置点击
    screenshot_request_signal = pyqtSignal(QRect)  # 请求截图
    screenshot_result_signal = pyqtSignal(object)  # 截图结果

    def __init__(self, app):
        super().__init__()
        self.app = app
        self._is_paused = False
        self._is_running = True
        self.processing = False  # 标志是否正在处理
        self.screenshot_event = threading.Event()
        self.screenshot_result = None

    def run(self):
        self.update_label_signal.emit("开始监控中...")
        self.log_signal.emit("正在启动自动回复功能...")
        logging.info("Monitoring thread started.")
        error_logged = False

        while self.is_running():
            if self.is_paused():
                time.sleep(1)
                continue

            try:
                # 仅当没有正在处理时才进行匹配
                if not self.processing:
                    chat_region = QRect(
                        self.app.chat_area[0],
                        self.app.chat_area[1],
                        self.app.chat_area[2],
                        self.app.chat_area[3],
                    )

                    self.screenshot_request_signal.emit(chat_region)
                    self.screenshot_event.clear()
                    self.screenshot_event.wait()
                    chat_screenshot = self.screenshot_result

                    if chat_screenshot is None:
                        self.log_signal.emit("无法获取消息区域的截图。")
                        logging.warning("Failed to get chat area screenshot.")
                        continue

                    chat_screenshot_pil = Image.fromqimage(chat_screenshot)
                    matches = []

                    for target_image in self.app.target_images:
                        try:
                            found = list(pyautogui.locateAll(
                                target_image.convert('RGB'),
                                chat_screenshot_pil.convert('RGB'),
                                confidence=0.8
                            ))
                            if found:
                                matches.extend(found)
                        except pyautogui.ImageNotFoundException:
                            pass

                    if matches:
                        match_positions = []
                        for match_location in matches:
                            x = int(self.app.chat_area[0] + match_location.left + match_location.width / 2)
                            y = int(self.app.chat_area[1] + match_location.top + match_location.height / 2)
                            match_positions.append((x, y))

                        self.log_signal.emit(f"检测到新的消息，准备自动回复...")
                        logging.debug(f"Found matches at positions: {match_positions}")
                        x, y = random.choice(match_positions)

                        self.processing = True  # 开始处理

                        self.click_position_signal.emit(x, y)
                        time.sleep(1)

                        conversation_region = QRect(
                            self.app.conversation_area[0],
                            self.app.conversation_area[1],
                            self.app.conversation_area[2],
                            self.app.conversation_area[3],
                        )

                        self.screenshot_request_signal.emit(conversation_region)
                        self.screenshot_event.clear()
                        self.screenshot_event.wait()
                        conversation_screenshot = self.screenshot_result

                        if conversation_screenshot is None:
                            self.log_signal.emit("无法获取会话区域的截图。")
                            logging.warning("Failed to get conversation area screenshot.")
                            self.processing = False  # 处理失败，重置标志
                            continue

                        screenshot_path = "latest_screenshot.png"
                        conversation_screenshot.save(screenshot_path)
                        self.log_signal.emit("正在生成回复，请稍候...")
                        logging.debug("Saved conversation screenshot.")

                        image_url = upload_image(screenshot_path, self.app.upload_token, self.app.upload_url)
                        if not image_url:
                            self.log_signal.emit("图片上传失败。")
                            self.processing = False
                            continue

                        ai_reply = upload_and_get_reply(
                            image_url,
                            self.app.role_personality,
                            self.app.knowledge_base,
                            self.app.api_key
                        )
                        self.log_signal.emit("回复已生成，正在发送...")
                        logging.debug("AI reply generated.")

                        self.input_reply_signal.emit(ai_reply)
                        # 等待回复输入和发送完成
                        QEventLoop().exec_()

                        self.processing = False  # 处理完成，重置标志
                    else:
                        if not error_logged:
                            self.log_signal.emit("暂无新消息，继续监控中...")
                            error_logged = True
                            logging.debug("No new messages found.")
                        time.sleep(1)
                else:
                    time.sleep(1)

            except Exception as e:
                if not error_logged:
                    self.log_signal.emit("自动回复功能遇到问题，正在尝试恢复...")
                    error_logged = True
                    self.processing = False  # 出现异常，重置标志
                    logging.exception("Exception in MonitoringThread run method.")
                time.sleep(1)

    def pause(self):
        self._is_paused = True
        self.log_signal.emit("已暂停自动回复功能。")
        logging.info("Monitoring thread paused.")

    def resume(self):
        self._is_paused = False
        self.log_signal.emit("已恢复自动回复功能。")
        logging.info("Monitoring thread resumed.")

    def stop(self):
        self._is_running = False
        self.log_signal.emit("已停止自动回复功能。")
        logging.info("Monitoring thread stopped.")

    def is_paused(self):
        return self._is_paused

    def is_running(self):
        return self._is_running

    def receive_screenshot(self, image):
        self.screenshot_result = image
        self.screenshot_event.set()
