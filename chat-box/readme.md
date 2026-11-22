# 情绪盒子 · Streamlit 聊天 Demo

基于 DeepSeek 的专属爱豆情绪陪伴聊天应用，支持多轮上下文与流式输出。

## 准备

1. 安装依赖（Python 3.10+）：

   ```bash
   pip install -r chat-box/requirements.txt
   ```

2. 在 `chat-box/` 下创建 `.env` 文件并写入 DeepSeek API Key（可直接复制 `.env.example` 修改）：

   ```
   API_KEY=你的密钥
   ```

## 运行

网页版（推荐）：

```bash
cd chat-box
streamlit run chatbox2.py
```

命令行版（无浏览器环境时使用）：

```bash
cd chat-box
python chatbox.py
```

## 功能

- 多轮对话：历史消息随每次请求发给模型，上下文连续
- 流式输出：回答逐字上屏
- 会话管理：网页版侧边栏一键清空对话
- 失败回滚：模型调用失败时本轮消息不入历史，下一轮上下文保持完整

## 说明

- `.env` 已被 gitignore，密钥不会入库
- 命令行版支持 `q` / `quit` / `exit` 退出
