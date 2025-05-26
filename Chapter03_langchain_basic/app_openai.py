import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import os

# 设置Ollama服务地址
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# 初始化Ollama LLM
try:
    llm = Ollama(model="qwen3:8b")
except Exception as e:
    st.error(f"初始化Ollama LLM失败，请确保Ollama服务正在运行，并且指定模型已下载。错误：{e}")
    st.stop()

st.title("基于 Ollama 和 Langchain 的问答系统")

# 定义提示模板
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="作为一个智能助手，你只需要回答医学相关的问题。当你回答用户问题时，需要先判断用户的问题是否与医学有关，如果用户问到无关医学问题，你必须回答我不知道。请回答以下问题：{question}。"
)

# 用户输入
user_question = st.text_input("请输入你的问题：")

if user_question:
    with st.spinner("大模型正在思考中..."):
        try:
            # 格式化提示
            formatted_prompt = prompt_template.format(question=user_question)
            print(formatted_prompt)
            response = llm.invoke(formatted_prompt)
            st.write("回答：")
            st.markdown(response)
        except Exception as e:
            st.error(f"调用Ollama LLM时出错：{e}")
