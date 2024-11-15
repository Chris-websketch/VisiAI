# utils/helper.py
from PyQt6.QtCore import QTimer
import pyautogui
import pyperclip
import logging

def perform_mouse_actions(x, y, click_callback):
    """在主线程中执行鼠标操作，不阻塞 GUI"""
    try:
        pyautogui.moveTo(x, y)
        logging.debug(f"Moved mouse to ({x}, {y})")
        QTimer.singleShot(500, click_callback)
    except Exception as e:
        logging.exception("Exception in perform_mouse_actions.")

def click_and_paste(paste_callback):
    """点击并粘贴文本"""
    try:
        pyautogui.click()
        logging.debug("Clicked mouse.")
        QTimer.singleShot(500, paste_callback)
    except Exception as e:
        logging.exception("Exception in click_and_paste.")

def paste_and_send(send_callback):
    """粘贴文本并发送"""
    try:
        pyautogui.hotkey('ctrl', 'v')
        logging.debug("Pasted reply.")
        QTimer.singleShot(500, send_callback)
    except Exception as e:
        logging.exception("Exception in paste_and_send.")

def press_enter():
    """按下回车键发送消息"""
    try:
        pyautogui.press('enter')
        logging.debug("Pressed enter to send reply.")
    except Exception as e:
        logging.exception("Exception in press_enter.")
