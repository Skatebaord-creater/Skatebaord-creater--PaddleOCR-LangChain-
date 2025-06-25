import json

from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import os
from openai import OpenAI

# def generate_next_response(chat_history_path='MorganLeGouar.json'):
#     # 读取聊天记录
#     # 拼接完整的文件路径
#     full_path = os.path.join('assets', chat_history_path)
#     # 读取聊天记录
#     chat_context = load_chat_history(full_path)
#     print(chat_context)
#     # 自定义 Prompt 模板
#     template = """
#     你是一个智能聊天助手。以下是用户与一个女孩的聊天记录：
#
#     {chat_history}
#
#     请基于这段聊天，生成一句合理的下一条回复：
#     """
#
#     prompt = PromptTemplate(
#         input_variables=["chat_history"],
#         template=template,
#     )
#
#     llm = Ollama(model='mistral')
#
#     chain = LLMChain(llm=llm, prompt=prompt)
#
#     response = chain.run({"chat_history": chat_context})
#
#     print("🧠 生成回复：", response)

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
# client = OpenAI(
#     # 此为默认路径，您可根据业务所在地域进行配置
#     base_url="https://ark.cn-beijing.volces.com/api/v3",
#     # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
#     api_key="7836e00a-5fa3-472a-b19b-2b64591c07ea",
# )

# def generate_next_response1(chat_history_path):
#         # full_path = os.path.join('../assets',  chat_history_path)
#          # 读取聊天记录
#         chat_context = load_chat_history(chat_history_path)
#         response = client.chat.completions.create(
#             # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
#             model="doubao-1-5-vision-pro-32k-250115",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": f"你是一个智能聊天助手。以下是完整的聊天记录：\n{chat_context}\n请基于这段完整的聊天，生成一句合理的下一条回复："
#                         }
#                     ]
#                 }
#             ],
#
#         )
#
#         print(f"🤖建议你回答 ： {response.choices[0].message.content}")

# 初始化Ark客户端，从环境变量中读取您的API Key
client = ChatOpenAI(
    # 此为默认路径，您可根据业务所在地域进行配置
    openai_api_base="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    openai_api_key="7836e00a-5fa3-472a-b19b-2b64591c07ea",
    model="doubao-1-5-vision-pro-32k-250115"
)

# 自定义结构化提示模板
myPromptTemplate = PromptTemplate(
    input_variables=["chat_history"],
    template="""
你是一个擅长社交心理学的恋爱聊天顾问，角色是“懂她又懂撩的朋友” —— 既能读懂她的情绪，又能制造暧昧心动的氛围。

🎯 你的目标是：
- 让她感受到被理解、被接纳，情绪上对你逐渐依赖；
- 轻松撩动她的心弦，建立暧昧张力；
- 不油腻、不讨好，让她逐渐“上头”，喜欢上你。

🧠 请分析以下聊天记录，并生成一条回复，使她**感觉你特别懂她，同时产生情绪依赖与好奇感，愿意继续亲密对话。**

💬 聊天记录 Chat History:
\"\"\"
{chat_history}
\"\"\"

📌 请使用以下结构输出：
1. ✨ 回复背后的情绪策略（如：共情 + 赞美 / 反差幽默 / 撩而不俗 / 安全感 + 小挑逗）
2. ❤️ 推荐回复内容（一句话或两句话，轻撩+懂她+制造张力）
"""
)


def load_chat_history(chat_history_path):
    """从JSON文件加载聊天历史并转换为LangChain消息格式"""
    with open(chat_history_path, 'r', encoding='utf-8') as f:
        chat_data = json.load(f)

    # 初始化Memory对象
    memory = ConversationBufferMemory(memory_key="chat_history")

    # 将每条消息添加到Memory中
    for msg in chat_data:
        if msg["role"] == "对方":
            memory.chat_memory.add_user_message(msg["text"])
        elif msg["role"] == "我":
            memory.chat_memory.add_ai_message(msg["text"])

    return memory
def generate_next_response1(chat_history_path):
    # 读取聊天记录
    chat_context = load_chat_history(chat_history_path)

    # 构造 Chain
    chain = LLMChain(llm=client, prompt=myPromptTemplate)

    # 运行 Chain，生成回复
    response = chain.run(chat_history=chat_context)

    print("🤖建议你回答：\n", response)

