# utils/image_utils.py
from PIL import Image
import pyautogui
import logging
import requests

def image_in_area(area_screenshot, target_image):
    """检查指定区域内是否包含目标图像"""
    try:
        # 确保图像为 RGB 模式
        area_screenshot = area_screenshot.convert('RGB')
        target_image = target_image.convert('RGB')

        result = pyautogui.locate(target_image, area_screenshot, confidence=0.8)
        return result is not None
    except Exception as e:
        logging.exception("Exception in image_in_area.")
        return False

def upload_image(image_path, upload_token, upload_url):
    """上传图片到服务器并返回图片 URL"""
    try:
        # 打开原始截图
        image = Image.open(image_path)
        # 获取图像尺寸
        width, height = image.size
        # 裁剪图像，只保留左半部分
        cropped_image = image.crop((0, 0, width // 2, height))
        # 保存裁剪后的图像到临时路径
        temp_image_path = "temp_cropped_image.png"
        cropped_image.save(temp_image_path)
        logging.debug(f"Image cropped and saved to {temp_image_path}")
        # 上传裁剪后的图像
        with open(temp_image_path, 'rb') as f:
            files = {'image': f}
            data = {'token': upload_token}
            response = requests.post(upload_url, files=files, data=data)
        logging.debug(f"Image uploaded, response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            image_url = result.get('url')
            if image_url:
                logging.debug(f"Image URL: {image_url}")
                return image_url
            else:
                logging.warning("Image upload failed, no URL returned.")
                return None
        else:
            logging.error(f"Image upload failed, status code: {response.status_code}")
            return None
    except Exception as e:
        logging.exception("Exception in upload_image.")
        return None
