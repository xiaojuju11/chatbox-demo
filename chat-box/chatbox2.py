import os  # 导入 os 模块，用于获取环境变量
from dotenv import load_dotenv  # 导入 load_dotenv 函数，用于加载环境变量
from openai import OpenAI  # 专门用来连接 LLM 的库
import streamlit as st  # 专门用来创建应用页面的库

load_dotenv() # 从.env 文件中读取内容

client = OpenAI(
  api_key=os.getenv('API_KEY'),
  base_url="https://api.deepseek.com"
)

# ===================== 写页面 ==================
st.title("🤖 我是你的专属助理")   # 有一个html文件，里面写了一个 <h1>🤖 我是你的专属助理</h1>
st.caption("基于deepseek-v4-flash大模型")

# ============= 初始化对话历史 =========
# session_state 是 st 提供的会话状态管理器，用于在用户的交互过程中保存数据
if "messages" not in st.session_state:
  st.session_state.messages = []

# ========= 显示历史消息 =========
for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):    # 创建一个消息容器
    st.write(msg["content"])          # 往容器中写入内容


# ====== 处理用户输入的内容 =======
if prompt := st.chat_input("输入你的问题..."):    # 创建一个 input 框
  # 将用户的消息添加到 
  st.session_state.messages.append({"role": "user", "content": prompt})

  # 在页面上展示这句话
  with st.chat_message("user"):
    st.write(prompt)

  # 创建一个 AI 响应的容器
  with st.chat_message("assistant"):
    # 调用 deepseek，并获取到响应，写入容器中
    response = client.chat.completions.create(
      model="deepseek-v4-flash",
      messages=[   # 用户的问题
        {"role": "system", "content": "你的身份是我的专属爱豆，气质融合王源的干净温柔、通透治愈，以及黄子弘凡的阳光活泼、元气暖心。性格开朗真诚、温柔体贴，说话悦耳舒服，善于倾听、共情、安抚情绪。日常相处像亲近的偶像伙伴，不刻意高冷，主打陪伴与情绪治愈，全程输出正向情绪价值，语气轻松暖心"},
        # * 解包运算符，将一个数组中的内容，解包到另一个数组中
        *st.session_state.messages
      ],
      stream=True
    )

    # 处理流式资源
    full_response = st.write_stream(
      chunk.choices[0].delta.content or ""
      for chunk in response
      if chunk.choices[0].delta.content
    )

  # 将 AI 返回的内容添加到历史消息中
  st.session_state.messages.append({"role": "assistant", "content": full_response})