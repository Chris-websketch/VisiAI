# utils/ai_api.py
import requests
import json
import logging

def upload_and_get_reply(image_url, role_personality, knowledge_base, api_key):
    """上传图片并获取 AI 回复"""
    try:
        # 按照指定格式构建 role_personality
        role_personality_full = f"{role_personality}，你在回答时请结合我的知识库，我的知识库是：{knowledge_base}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": role_personality_full},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ]

        url = "http://proxy.5fgo2v.top/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",  # 请替换为您的实际 API 密钥
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": 300
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        # 提取 AI 回复内容
        ai_reply_text = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
        logging.debug("AI reply received.")
        return ai_reply_text
    except Exception as e:
        logging.exception("Exception in upload_and_get_reply.")
        return "抱歉，暂时无法处理您的请求。"
