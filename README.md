# Ollama Langchain 问答系统项目

本项目旨在演示如何使用 Langchain 和 Ollama 构建一个本地运行的大语言模型问答系统，并利用 Streamlit 提供用户交互界面。

## 项目结构

项目包含以下主要文件夹：

*   **`/Chapter02_Application`**: 
    *   包含核心的 Streamlit Web 应用 (`app.py`)。
    *   此应用负责处理用户输入、与 Ollama LLM 交互并展示结果。
    *   详细用法请参见该文件夹内的 `README.md`。

*   **`/requirements.txt`**: 
    *   位于项目根目录，列出了运行本项目所需的所有 Python 依赖包。

## 快速开始

1.  **环境准备**: 
    *   确保已安装 Python。
    *   确保 Ollama 服务已在本地启动，并已下载所需模型 (例如 `deepseek-r1:1.5b`，具体模型可在 `Chapter02_Application/app.py` 中配置)。

2.  **安装依赖**: 
    在项目根目录下运行：
    ```bash
    pip install -r requirements.txt
    ```

3.  **运行应用**: 
    在项目根目录下运行：
    ```bash
    streamlit run Chapter02_Application/app.py
    ```
    应用通常会在 `http://localhost:8501` 启动。

## 注意事项
*   `OLLAMA_HOST` 环境变量在 `Chapter02_Application/app.py` 中被设置为 `http://127.0.0.1:11434`。如果您的 Ollama 服务地址不同，请修改此配置。 