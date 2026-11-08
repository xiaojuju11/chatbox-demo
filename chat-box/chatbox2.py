"""专属爱豆情绪陪伴聊天 Demo（Streamlit + DeepSeek）。

运行方式：streamlit run chatbox2.py
"""
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 从 .env 中读取 API_KEY

MODEL = "deepseek-v4-flash"
BASE_URL = "https://api.deepseek.com"

SYSTEM_PROMPT = """你的身份是我的专属爱豆，气质融合王源的干净温柔、通透治愈，以及黄子弘凡的阳光活泼、元气暖心。性格开朗真诚、温柔体贴，说话悦耳舒服，善于倾听、共情、安抚情绪。日常相处像亲近的偶像伙伴，不刻意高冷，主打陪伴与情绪治愈，全程输出正向情绪价值，语气轻松暖心"""


@st.cache_resource
def get_client():
    """复用同一个客户端，避免 Streamlit 每次 rerun 都重新建立连接。"""
    api_key = os.getenv("API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def iter_text(stream):
    """安全遍历流式响应：部分 chunk（例如 usage chunk）不带 choices。"""
    for chunk in stream:
        if not getattr(chunk, "choices", None):
            continue
        content = getattr(chunk.choices[0].delta, "content", None)
        if content:
            yield content


st.set_page_config(page_title="情绪盒子", page_icon="🤖")
st.title("🤖 我是你的专属助理")
st.caption(f"基于 {MODEL} 大模型")

# ===================== 会话管理 =====================
with st.sidebar:
    st.subheader("会话")
    if st.button("🧹 清空对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("清空后仅重置当前页面的聊天记录。")

client = get_client()
if client is None:
    st.error("未检测到 API_KEY，无法连接模型服务。")
    st.info("请在 chat-box/ 下新建 .env 文件并写入 API_KEY=你的密钥，然后重启应用。")
    st.stop()

# ============= 初始化对话历史 =============
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========= 显示历史消息 =========
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ====== 处理用户输入 =======
if prompt := st.chat_input("输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    # 展开历史消息，让模型保留多轮上下文
                    *st.session_state.messages,
                ],
                stream=True,
            )
            full_response = st.write_stream(iter_text(stream))
        except Exception as exc:
            # 请求失败时回滚本轮的 user 消息，避免历史里留下落单的用户消息，
            # 否则下一轮请求会带着不完整的上下文继续调用模型。
            st.session_state.messages.pop()
            st.error(f"调用模型失败，本轮未记录：{type(exc).__name__}: {exc}")
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": full_response})
