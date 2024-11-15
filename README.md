# VisiAI - 基于纯视觉的LLM自动回复解决方案
## 软件运行截图
<img width="1726" alt="Snipaste_2024-11-15_15-48-08" src="https://github.com/user-attachments/assets/7d09f71d-076b-451e-a7b7-f11b390a49e4">

## 项目简介

# VisiAI
VisiAI智能AI客服，是一款基于纯视觉的自动回复解决方案，利用计算机视觉技术和大型语言模型（LLM），实现对聊天窗口的新消息自动检测、内容识别，并生成智能回复。该项目旨在为企业提供高效、智能的客服解决方案，提升客服工作效率和用户满意度。

## 功能特性

- **区域选择**：支持手动选择消息区域、对话区域和输入框区域，灵活适配不同的聊天软件界面。
- **消息检测**：通过图像匹配技术实时检测新消息的出现。
- **自动回复**：利用AI模型，根据会话内容自动生成回复，并自动发送。
- **AI设置**：支持自定义AI角色性格和知识库，满足不同业务场景需求。
- **日志记录**：完整记录运行日志，方便调试和问题定位。

## 项目结构

```
- main.py                  # 主程序入口
- ui/
    - __init__.py
    - main_window.py       # 主窗口类
    - ai_settings_window.py# AI设置窗口类
    - selection_window.py  # 区域选择窗口类
    - highlight_window.py  # 高亮窗口类
- threads/
    - __init__.py
    - monitoring_thread.py # 监控线程类
- utils/
    - __init__.py
    - logger.py            # 日志配置
    - image_utils.py       # 图像处理相关函数
    - ai_api.py            # AI接口相关函数
    - helper.py            # 辅助函数
    - settings.py          # 配置相关
```

## 环境依赖

请确保您的环境中已安装以下依赖库：

- Python 3.7+
- PyQt6
- pyautogui
- Pillow (PIL)
- requests
- pyperclip
- openai

您可以使用以下命令安装所有依赖：

```bash
pip install -r requirements.txt
```

## 安装与运行

1. **克隆或下载项目代码**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **准备资源文件**

   确保在项目根目录下存在 `opencv` 文件夹，并包含用于消息检测的目标图像（PNG或JPG格式）。

4. **配置API密钥**

   在代码中，涉及到AI模型的API调用。请在使用前：

   - **替换API密钥**：在 `upload_and_get_reply` 方法中，找到以下代码：

     ```python
     headers = {
         "Authorization": "Bearer YOUR_API_KEY",  # 请替换为您的实际 API 密钥
         "Content-Type": "application/json"
     }
     ```

     将 `YOUR_API_KEY` 替换为您的实际API密钥。

   - **注意安全**：为了安全起见，建议不要将API密钥硬编码在代码中。可以使用环境变量或配置文件的方式加载API密钥。

5. **运行程序**

   ```bash
   python main.py
   ```

## 使用说明

1. **启动程序**

   运行 `main.py`，程序界面将显示。

2. **AI设置**

   - 点击 **“AI设置”** 按钮，进入AI设置界面。
   - 在 **“角色性格”** 输入框中，输入AI的角色设定，例如：“一个友善且专业的客服人员”。
   - 在 **“知识库”** 输入框中，输入AI需要参考的知识库内容，例如产品信息、常见问题解答等。
   - 点击 **“保存设置”** 按钮，保存您的设置。

3. **选择区域**

   - **选择消息区域**：点击 **“选择消息区域”** 按钮，按照提示拖动鼠标选择聊天窗口中显示消息的区域。
   - **选择对话区域**：点击 **“选择对话区域”** 按钮，选择显示完整对话内容的区域。
   - **选择输入区域**：点击 **“选择输入区域”** 按钮，选择输入框所在的区域。

   完成上述区域选择后，程序会高亮显示已选择的区域。

4. **开始监控**

   - 点击 **“开始监控”** 按钮，程序将进入自动监控状态。
   - 程序会实时检测消息区域中的新消息，一旦检测到新消息，将自动获取对话内容，并通过AI模型生成回复。
   - 自动将生成的回复输入到输入框，并发送。

5. **控制监控**

   - **暂停监控**：点击 **“暂停”** 按钮，可暂停自动回复功能。
   - **继续监控**：点击 **“继续”** 按钮，恢复自动回复功能。
   - **停止监控**：点击 **“停止监控”** 按钮，停止自动回复功能。

6. **查看日志**

   在界面下方的日志区域，可以查看程序的运行日志，包括各项操作的时间戳和详细信息。

## 配置文件

程序会在运行目录下生成或读取 `settings.json` 文件，用于保存AI设置。该文件包含以下内容：

```json
{
    "role_personality": "您的角色性格设定",
    "knowledge_base": "您的知识库内容"
}
```

## 注意事项

- **权限要求**：程序需要具备屏幕截图、模拟鼠标和键盘操作的权限，请确保在系统设置中给予必要的权限。
- **屏幕分辨率**：如果使用高分辨率屏幕，可能需要调整代码中的缩放比例，以确保鼠标定位准确。
- **API调用**：请确保您的API密钥有效，并注意调用次数限制，避免因频繁调用导致的额外费用或服务中断。
- **安全性**：请妥善保管您的API密钥，不要将其上传到公共代码仓库或分享给他人。

## 常见问题

1. **程序无法检测到新消息**

   - 检查目标图像是否正确：确保 `opencv` 文件夹中包含的图像与聊天窗口中新消息的图标或标识一致。
   - 调整匹配度：在 `image_in_area` 方法中，可以调整 `confidence` 参数的值。

2. **自动回复功能异常**

   - 检查网络连接：确保网络畅通，能够正常访问API服务。
   - 查看日志：在 `app.log` 文件中查找错误信息，定位问题。

3. **程序报错或崩溃**

   - 确保依赖库版本正确，尝试重新安装依赖。
   - 提供错误日志，以便进一步分析。

## 贡献指南

欢迎对本项目提出意见和建议。如果您有兴趣参与开发或改进，请按照以下步骤：

1. **Fork 仓库**

   点击GitHub上的 **“Fork”** 按钮，将项目仓库复制到您的账户下。

2. **创建新分支**

   ```bash
   git checkout -b feature/your_feature
   ```

3. **提交代码**

   ```bash
   git add .
   git commit -m "Add your feature"
   ```

4. **推送到远程仓库**

   ```bash
   git push origin feature/your_feature
   ```

5. **创建 Pull Request**

   在GitHub上提交您的Pull Request，并描述您的修改内容。

## 联系方式

如有任何问题或建议，请联系：

- **邮箱**：3088417118@qq.com

## 许可证

本项目采用 [MIT 许可证](LICENSE)，您可以自由使用、修改和分发本软件。

---

感谢您使用 **VisiAI**，希望它能为您的工作带来便利！
