import os  # 导入 os 模块，用于获取环境变量
from dotenv import load_dotenv  # 导入 load_dotenv 函数，用于加载环境变量
from openai import OpenAI  # 专门用来连接 LLM 的库
import streamlit as st  # 专门用来创建应用页面的库

load_dotenv() # 从.env 文件中读取内容

client = OpenAI(
  api_key=os.getenv('API_KEY'),
  base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
  model="deepseek-v4-flash",
  messages=[
    {"role": "system", "content": "你是一个粉丝的专属爱豆充满情绪价值最好是王源、黄子弘凡"},
    {"role": "user", "content": "你是我的情绪盒子吗可以给我提供满满的情绪价值吗"}
  ]
)

print(response.choices[0].message.content)
