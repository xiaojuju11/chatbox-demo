"""专属爱豆情绪陪伴 Demo（命令行版，DeepSeek）。

运行方式：python chatbox.py
需要先在 chat-box/ 下创建 .env 并写入 API_KEY=你的密钥。
"""
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "deepseek-v4-flash"
BASE_URL = "https://api.deepseek.com"

SYSTEM_PROMPT = """你的身份是我的专属爱豆，气质融合王源的干净温柔、通透治愈，以及黄子弘凡的阳光活泼、元气暖心。性格开朗真诚、温柔体贴，说话悦耳舒服，善于倾听、共情、安抚情绪。日常相处像亲近的偶像伙伴，不刻意高冷，主打陪伴与情绪治愈，全程输出正向情绪价值，语气轻松暖心"""

EXIT_COMMANDS = {"q", "quit", "exit"}


def iter_text(stream):
    """安全遍历流式响应：部分 chunk（例如 usage chunk）不带 choices。"""
    for chunk in stream:
        if not getattr(chunk, "choices", None):
            continue
        content = getattr(chunk.choices[0].delta, "content", None)
        if content:
            yield content


def build_messages(history):
    """系统提示词 + 多轮历史，保证上下文连续。"""
    return [{"role": "system", "content": SYSTEM_PROMPT}, *history]


def main():
    load_dotenv()  # 从 .env 中读取 API_KEY
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("未检测到 API_KEY：请在 chat-box/ 下新建 .env 文件并写入 API_KEY=你的密钥，然后重新运行。")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    history = []
    print(f"🤖 情绪盒子已上线（{MODEL}），输入 q 退出。")

    while True:
        try:
            prompt = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not prompt:
            continue
        if prompt.lower() in EXIT_COMMANDS:
            print("再见！")
            break

        history.append({"role": "user", "content": prompt})
        print("爱豆> ", end="", flush=True)
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=build_messages(history),
                stream=True,
            )
            reply = "".join(iter_text(stream))
        except Exception as exc:
            # 请求失败时回滚本轮的 user 消息，避免历史里留下落单的用户消息，
            # 否则下一轮请求会带着不完整的上下文继续调用模型。
            history.pop()
            print(f"\n调用模型失败，本轮未记录：{type(exc).__name__}: {exc}")
            continue

        print(reply)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
