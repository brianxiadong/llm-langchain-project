import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import os

from langchain_openai import ChatOpenAI

# 从环境变量获取API密钥，如果没有则使用Streamlit输入框
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    st.warning("请设置OPENAI_API_KEY环境变量或在下方输入API密钥")
    api_key = st.text_input("OpenAI API密钥:", type="password")
    if not api_key:
        st.stop()

os.environ["OPENAI_API_KEY"] = api_key

# 设置Ollama服务地址
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# 初始化OpenAI LLM
try:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
except Exception as e:
    st.error(f"初始化OpenAI LLM失败：{e}")
    st.stop()

st.title("基于 OpenAI 和 Langchain 的问答系统")

# 定义提示模板
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="请回答以下问题：{question}。"
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
            st.markdown(response.content)
        except Exception as e:
            st.error(f"调用OpenAI LLM时出错：{e}")
