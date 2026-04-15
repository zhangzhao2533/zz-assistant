from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMemory

def get_conversation_memory() -> BaseMemory:
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )