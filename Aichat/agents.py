from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import ChatTongyi

load_dotenv()


MODEL_NAME = "qwen-plus-2025-09-11"

llm = ChatTongyi(model_name=MODEL_NAME
                 ,streaming=True
                 ,model_kwargs={
                       "temperature": 0.7,  # 核心参数：控制随机性，0-1之间，推荐0.5-0.8
                        "top_p": 0.9,        # 配合temperature使用，一般设0.9即可
                        "seed": None         # 如果想偶尔换答案，可设随机seed（如123/456），None则每次随机
                 }
                 )

