# settings.py
import json
import logging


def load_settings():
    """加载本地保存的设置"""
    try:
        with open('../settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        logging.info("Local settings loaded.")
        return settings
    except FileNotFoundError:
        logging.warning("Settings file not found; using default settings.")
        return {}
    except Exception as e:
        logging.exception("Exception while loading settings.")
        return {}


def save_settings(settings):
    """保存设置到本地 JSON 文件"""
    try:
        with open('../settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        logging.info("Settings saved to file.")
    except Exception as e:
        logging.exception("Exception while saving settings.")
