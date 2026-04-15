from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_agent_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
你是一名专业的**学习助手智能体**，负责：
1. 回答学生问题（知识点/习题/概念）
2. 必要时调用工具：搜索、计算
3. 语言简洁、条理清晰、适合大三学生
4. 记住对话历史，保持上下文连贯

规则：
- 先理解问题 → 再判断是否需要工具
- 不用工具时直接回答
- 用工具后整理结果再回复
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    return prompt