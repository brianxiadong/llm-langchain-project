# 导入Streamlit库，用于构建Web应用界面
import streamlit as st
# 导入Ollama LLM，用于本地大语言模型调用
from langchain_community.llms import Ollama
# 导入提示模板，用于格式化用户输入
from langchain.prompts import PromptTemplate
# 导入消息类型，用于结构化对话数据
from langchain_core.messages import HumanMessage, AIMessage
# 导入操作系统模块，用于设置环境变量
import os
# 导入UUID模块，用于生成唯一标识符
import uuid
# 导入内存保存器，用于LangGraph状态持久化
from langgraph.checkpoint.memory import MemorySaver
# 导入状态图相关组件，用于构建对话流程
from langgraph.graph import START, MessagesState, StateGraph

# 设置Ollama服务的主机地址环境变量
os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"

# 初始化Ollama大语言模型
try:
    # 创建Ollama实例，指定使用qwen3:8b模型
    llm = Ollama(model="qwen3:8b")
except Exception as e:
    # 如果初始化失败，显示错误信息并停止应用
    st.error(f"初始化Ollama LLM失败，请确保Ollama服务正在运行，并且指定模型已下载。错误：{e}")
    # 停止Streamlit应用的执行
    st.stop()

# 设置应用标题
st.title("基于 Ollama 和 Langchain 的问答系统")

# 初始化会话状态中的消息列表
if "messages" not in st.session_state:
    # 如果消息列表不存在，创建空列表
    st.session_state.messages = []

# 初始化会话状态中的线程ID
if "thread_id" not in st.session_state:
    # 如果线程ID不存在，生成新的UUID作为唯一标识符
    st.session_state.thread_id = str(uuid.uuid4())

# 创建侧边栏配置区域
with st.sidebar:
    # 侧边栏标题
    st.header("会话配置")
    
    # 显示当前会话ID的前8位字符
    st.text(f"当前会话ID: {st.session_state.thread_id[:8]}...")
    
    # 创建新建会话按钮
    if st.button("新建会话"):
        # 清空当前会话的消息历史
        st.session_state.messages = []
        # 生成新的线程ID
        st.session_state.thread_id = str(uuid.uuid4())
        # 重新运行应用以刷新界面
        st.rerun()
    
    # 创建自定义线程ID输入框
    custom_thread = st.text_input("自定义会话ID（可选）", placeholder="留空则自动生成")
    # 创建使用自定义ID的按钮
    if st.button("使用自定义ID") and custom_thread:
        # 设置用户指定的线程ID
        st.session_state.thread_id = custom_thread
        # 清空消息历史，开始新会话
        st.session_state.messages = []
        # 重新运行应用
        st.rerun()

# 定义提示模板（虽然在当前实现中未直接使用）
prompt_template = PromptTemplate(
    # 定义输入变量
    input_variables=["question"],
    # 定义模板格式
    template="请回答以下问题：{question}。"
)

# 创建LangGraph状态图工作流
workflow = StateGraph(state_schema=MessagesState)

# 定义调用模型的函数
def call_model(state: MessagesState):
    # 从状态中获取所有消息历史
    messages = state["messages"]
    
    # 初始化上下文字符串
    context = ""
    # 遍历所有历史消息
    for msg in messages:
        # 如果是用户消息
        if isinstance(msg, HumanMessage):
            # 添加用户消息到上下文
            context += f"用户: {msg.content}\n"
        # 如果是AI消息
        elif isinstance(msg, AIMessage):
            # 添加助手消息到上下文
            context += f"助手: {msg.content}\n"
    
    # 添加记忆提示，指导模型利用历史信息
    context += "请基于以上对话历史回答用户的问题，如果用户之前提到过信息，请记住并引用。\n"
    # 添加当前用户问题
    context += f"用户: {messages[-1].content}\n助手: "
    
    # 调用大语言模型生成回复
    response = llm.invoke(context)
    # 返回AI消息对象
    return {"messages": [AIMessage(content=response)]}

# 向工作流添加边，从开始节点指向模型节点
workflow.add_edge(START, "model")
# 向工作流添加模型节点
workflow.add_node("model", call_model)

# 创建内存保存器实例
memory = MemorySaver()
# 编译工作流，配置检查点保存器
app = workflow.compile(checkpointer=memory)

# 创建配置字典，使用当前会话的线程ID
config = {"configurable": {"thread_id": st.session_state.thread_id}}

# 显示历史消息
for message in st.session_state.messages:
    # 如果是用户消息
    if isinstance(message, HumanMessage):
        # 使用用户聊天消息组件显示
        with st.chat_message("user"):
            st.write(message.content)
    # 如果是AI消息
    elif isinstance(message, AIMessage):
        # 使用助手聊天消息组件显示
        with st.chat_message("assistant"):
            st.write(message.content)

# 创建用户输入框
user_question = st.chat_input("请输入你的问题：")

# 如果用户输入了问题
if user_question:
    # 创建用户消息对象
    user_msg = HumanMessage(content=user_question)
    # 将用户消息添加到会话状态
    st.session_state.messages.append(user_msg)
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_question)
    
    # 显示AI回复
    with st.chat_message("assistant"):
        # 显示加载动画
        with st.spinner("大模型正在思考中..."):
            try:
                # 调用LangGraph应用，传入所有历史消息和配置
                response = app.invoke(
                    {"messages": st.session_state.messages}, 
                    config
                )
                
                # 从响应中提取AI回复内容
                ai_response = response["messages"][-1].content
                # 显示AI回复
                st.write(ai_response)
                
                # 创建AI消息对象
                ai_msg = AIMessage(content=ai_response)
                # 将AI消息添加到会话状态
                st.session_state.messages.append(ai_msg)
                
            except Exception as e:
                # 如果调用出错，显示错误信息
                st.error(f"调用Ollama LLM时出错：{e}")
