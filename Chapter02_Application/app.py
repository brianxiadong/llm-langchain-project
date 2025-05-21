import streamlit as st # 导入Streamlit库，用于创建Web应用界面
from langchain_community.llms import Ollama # 从langchain_community.llms模块导入Ollama类，用于与Ollama大模型交互
import os # 导入os模块，用于与操作系统交互，如此处用于设置环境变量

# 设置Ollama服务地址
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434" # 设置环境变量OLLAMA_HOST，指定Ollama服务的API端点

# 初始化Ollama LLM
# 请确保你已经在Ollama中下载了一个模型，例如 llama2
# 你可以通过 `ollama list` 查看可用的模型
# 如果没有模型，可以通过 `ollama pull llama2` (或其他模型名) 下载
try: # 尝试执行以下代码块
    llm = Ollama(model="deepseek-r1:1.5b") # 初始化Ollama类，指定使用的模型名称（例如"deepseek-r1:1.5b"）。用户可以根据自己Ollama中已有的模型进行修改。
except Exception as e: # 如果在try代码块中发生任何异常
    st.error(f"初始化Ollama LLM失败，请确保Ollama服务正在运行，并且指定模型已下载。错误：{e}") # 在Streamlit界面上显示错误信息，提示用户检查Ollama服务和模型
    st.stop() # 停止Streamlit应用的执行

st.title("基于 Ollama 和 Langchain 的问答系统") # 设置Streamlit应用的标题

# 用户输入
user_question = st.text_input("请输入你的问题：") # 在Streamlit界面上创建一个文本输入框，让用户输入问题，并将输入内容存储在user_question变量中

if user_question: # 判断用户是否输入了问题 (即user_question是否不为空)
    with st.spinner("大模型正在思考中..."): # 在Streamlit界面上显示一个加载提示，告知用户模型正在处理
        try: # 尝试执行以下代码块
            response = llm.invoke(user_question) # 调用Ollama LLM的invoke方法，将用户的问题传递给模型，并获取模型的回答
            st.write("回答：") # 在Streamlit界面上显示"回答："文本
            st.markdown(response) # 使用markdown格式在Streamlit界面上显示模型的回答内容
        except Exception as e: # 如果在try代码块中发生任何异常 (例如调用LLM时出错)
            st.error(f"调用Ollama LLM时出错：{e}") # 在Streamlit界面上显示错误信息 