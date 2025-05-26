import streamlit as st
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import os
import uuid
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# 设置Ollama服务地址
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# 初始化Ollama LLM
try:
    llm = Ollama(model="qwen3:8b")
except Exception as e:
    st.error(f"初始化Ollama LLM失败，请确保Ollama服务正在运行，并且指定模型已下载。错误：{e}")
    st.stop()

st.title("基于 Ollama 和 Langchain 的问答系统")

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 初始化线程ID
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# 侧边栏配置
with st.sidebar:
    st.header("会话配置")
    
    # 显示当前线程ID
    st.text(f"当前会话ID: {st.session_state.thread_id[:8]}...")
    
    # 新建会话按钮
    if st.button("新建会话"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
    
    # 自定义线程ID选项
    custom_thread = st.text_input("自定义会话ID（可选）", placeholder="留空则自动生成")
    if st.button("使用自定义ID") and custom_thread:
        st.session_state.thread_id = custom_thread
        st.session_state.messages = []
        st.rerun()

# 定义提示模板
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="请回答以下问题：{question}。"
)

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define the function that calls the model
def call_model(state: MessagesState):
    # 获取所有消息历史
    messages = state["messages"]
    
    # 构建包含历史对话的完整上下文
    context = ""
    for msg in messages:
        if isinstance(msg, HumanMessage):
            context += f"用户: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            context += f"助手: {msg.content}\n"
    
    # 添加当前问题的提示
    context += "请基于以上对话历史回答用户的问题，如果用户之前提到过信息，请记住并引用。\n"
    context += f"用户: {messages[-1].content}\n助手: "
    
    # 调用模型
    response = llm.invoke(context)
    # 返回AI消息
    return {"messages": [AIMessage(content=response)]}

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 使用动态线程ID
config = {"configurable": {"thread_id": st.session_state.thread_id}}

# 显示历史消息
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

# 用户输入
user_question = st.chat_input("请输入你的问题：")

if user_question:
    # 添加用户消息到会话状态
    user_msg = HumanMessage(content=user_question)
    st.session_state.messages.append(user_msg)
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_question)
    
    with st.chat_message("assistant"):
        with st.spinner("大模型正在思考中..."):
            try:
                # 调用模型，传入所有历史消息
                response = app.invoke(
                    {"messages": st.session_state.messages}, 
                    config
                )
                
                # 获取AI回复
                ai_response = response["messages"][-1].content
                st.write(ai_response)
                
                # 添加AI消息到会话状态
                ai_msg = AIMessage(content=ai_response)
                st.session_state.messages.append(ai_msg)
                
            except Exception as e:
                st.error(f"调用Ollama LLM时出错：{e}")
