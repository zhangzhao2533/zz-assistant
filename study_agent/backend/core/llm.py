from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from dotenv import load_dotenv
import os

load_dotenv()

class QwenChatModel(BaseChatModel):
    model_name: str = "qwen3-max"
    api_key: str = ""
    base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    temperature: float = 0.3
    max_tokens: int = 1024

    def _generate(self, messages: list[BaseMessage], stop=None, run_manager=None, **kwargs):
        from openai import OpenAI
        
        client = OpenAI(
            api_key=self.api_key if self.api_key else os.getenv('DASHSCOPE_API_KEY'),
            base_url=self.base_url
        )
        
        openai_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                openai_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                openai_messages.append({"role": "assistant", "content": msg.content})
        
        response = client.chat.completions.create(
            model=self.model_name,
            messages=openai_messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        
        content = response.choices[0].message.content
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])

    @property
    def _llm_type(self):
        return "qwen3-max"

def get_llm(model_name: str = "qwen3-max") -> BaseChatModel:
    if model_name == "qwen3-max":
        return QwenChatModel(
            model_name="qwen3-max",
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            temperature=0.3,
            max_tokens=1024
        )
    else:
        raise ValueError("不支持的模型")