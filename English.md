# VisiAI - Vision-Based LLM Auto-Reply Solution

## Project Overview

**VisiAI** is an intelligent AI customer service solution that uses computer vision and large language models (LLMs) to automatically detect new messages in chat windows, recognize content, and generate intelligent replies. This project aims to provide businesses with an efficient and smart customer service solution, enhancing both efficiency and user satisfaction.

## Features

- **Area Selection**: Manually select message, conversation, and input box areas to adapt to different chat software interfaces.
- **Message Detection**: Real-time detection of new messages using image matching technology.
- **Auto Reply**: Generate replies using AI models based on conversation content and send them automatically.
- **AI Settings**: Customize AI personality and knowledge base to suit different business scenarios.
- **Log Recording**: Complete log recording for easy debugging and issue tracking.

## Project Structure

```
- main.py                  # Main program entry
- ui/
    - __init__.py
    - main_window.py       # Main window class
    - ai_settings_window.py# AI settings window class
    - selection_window.py  # Area selection window class
    - highlight_window.py  # Highlight window class
- threads/
    - __init__.py
    - monitoring_thread.py # Monitoring thread class
- utils/
    - __init__.py
    - logger.py            # Logging configuration
    - image_utils.py       # Image processing functions
    - ai_api.py            # AI API functions
    - helper.py            # Helper functions
    - settings.py          # Configuration related
```

## Environment Dependencies

Ensure the following dependencies are installed:

- Python 3.7+
- PyQt6
- pyautogui
- Pillow (PIL)
- requests
- pyperclip
- openai

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## Installation and Running

1. **Clone or Download the Project Code**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Resource Files**

   Ensure the `opencv` folder exists in the project root directory and contains target images (PNG or JPG format) for message detection.

4. **Configure API Key**

   For AI model API calls:

   - **Replace API Key**: In the `upload_and_get_reply` method, find the following code:

     ```python
     headers = {
         "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
         "Content-Type": "application/json"
     }
     ```

     Replace `YOUR_API_KEY` with your actual API key.

   - **Security Note**: Avoid hardcoding the API key in the code. Use environment variables or configuration files to load the API key.

5. **Run the Program**

   ```bash
   python main.py
   ```

## Usage Instructions

1. **Start the Program**

   Run `main.py` to display the program interface.

2. **AI Settings**

   - Click the **“AI Settings”** button to enter the AI settings interface.
   - Enter the AI's role in the **“Role Personality”** input box, e.g., “a friendly and professional customer service representative.”
   - Enter the knowledge base content in the **“Knowledge Base”** input box, such as product information or FAQs.
   - Click the **“Save Settings”** button to save your settings.

3. **Select Areas**

   - **Select Message Area**: Click the **“Select Message Area”** button and drag the mouse to select the area displaying messages in the chat window.
   - **Select Conversation Area**: Click the **“Select Conversation Area”** button to select the area displaying the full conversation content.
   - **Select Input Area**: Click the **“Select Input Area”** button to select the input box area.

   After completing the area selection, the program will highlight the selected areas.

4. **Start Monitoring**

   - Click the **“Start Monitoring”** button to begin automatic monitoring.
   - The program will detect new messages in the message area in real-time, retrieve conversation content, and generate replies using the AI model.
   - Automatically input and send the generated reply.

5. **Control Monitoring**

   - **Pause Monitoring**: Click the **“Pause”** button to pause the auto-reply function.
   - **Resume Monitoring**: Click the **“Continue”** button to resume the auto-reply function.
   - **Stop Monitoring**: Click the **“Stop Monitoring”** button to stop the auto-reply function.

6. **View Logs**

   View the program's running logs, including timestamps and detailed information of operations, in the log area at the bottom of the interface.

## Configuration File

The program will generate or read a `settings.json` file in the running directory to save AI settings. This file includes:

```json
{
    "role_personality": "Your role personality setting",
    "knowledge_base": "Your knowledge base content"
}
```

## Notes

- **Permissions**: The program requires permissions for screen capture, and simulating mouse and keyboard operations. Ensure necessary permissions are granted in system settings.
- **Screen Resolution**: Adjust the scaling ratio in the code if using a high-resolution screen to ensure accurate mouse positioning.
- **API Calls**: Ensure your API key is valid and be mindful of call limits to avoid extra charges or service interruptions.
- **Security**: Safeguard your API key and avoid uploading it to public repositories or sharing it with others.

## Common Issues

1. **Program Cannot Detect New Messages**

   - Check if the target image is correct: Ensure the images in the `opencv` folder match the new message icon or identifier in the chat window.
   - Adjust matching confidence: Modify the `confidence` parameter value in the `image_in_area` method.

2. **Auto-Reply Function Malfunction**

   - Check network connection: Ensure network connectivity for accessing API services.
   - Check logs: Locate errors in the `app.log` file for troubleshooting.

3. **Program Errors or Crashes**

   - Verify the correct version of dependencies and try reinstalling them.
   - Provide error logs for further analysis.

## Contribution Guidelines

We welcome feedback and suggestions for this project. If you're interested in contributing, follow these steps:

1. **Fork the Repository**

   Click the **“Fork”** button on GitHub to copy the repository to your account.

2. **Create a New Branch**

   ```bash
   git checkout -b feature/your_feature
   ```

3. **Commit Your Code**

   ```bash
   git add .
   git commit -m "Add your feature"
   ```

4. **Push to Remote Repository**

   ```bash
   git push origin feature/your_feature
   ```

5. **Create a Pull Request**

   Submit your Pull Request on GitHub and describe your changes.

## Contact

For any issues or suggestions, please contact:

- **Email**: 3088417118@qq.com

## License

This project is licensed under the [MIT License](LICENSE), allowing free use, modification, and distribution.

---

Thank you for using **VisiAI**. We hope it brings convenience to your work!
