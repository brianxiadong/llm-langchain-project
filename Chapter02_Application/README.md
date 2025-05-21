# Chapter 2: Application (`app.py`)

本文件夹包含项目的核心 Streamlit 应用代码 `app.py`。

## `app.py`

`app.py` 文件是使用 Streamlit 构建的问答系统用户界面和后端逻辑。

### 主要功能:
*   **连接 Ollama**: 初始化并连接到本地运行的 Ollama 服务。
    *   默认连接到 `http://127.0.0.1:11434`。
    *   默认使用的 Ollama 模型是 `deepseek-r1:1.5b` (可在代码中修改)。
*   **用户交互**: 提供一个文本输入框供用户提问。
*   **获取与显示**: 将用户问题发送给 Ollama 模型，获取回答，并在界面上显示出来。
*   **错误处理**: 对Ollama初始化和调用过程中的潜在错误进行捕获和提示。

### 如何运行 `app.py`

1.  **确保前提条件满足**:
    *   Python 环境已配置。
    *   Ollama 服务正在本地运行 (通常在 `http://127.0.0.1:11434`)。
    *   Ollama 中已下载所需模型 (例如 `deepseek-r1:1.5b` 或您在代码中指定的其他模型)。如果模型不存在，请先通过 `ollama pull <model_name>` 下载。
    *   项目根目录下的 `requirements.txt` 中的依赖已安装 (`pip install -r requirements.txt`)。

2.  **运行命令**:
    在项目的 **根目录** (不是 `Chapter02_Application` 目录)下执行以下命令来启动应用:
    ```bash
    streamlit run Chapter02_Application/app.py
    ```

应用启动后，通常可以在浏览器中通过 `http://localhost:8501` 访问。 