from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class StudyAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
        )
        self.chat_history = []
        self.tools = self._get_tools()
        self.system_prompt = self._get_system_prompt()

    def _get_tools(self):
        def web_search(query):
            try:
                from langchain_community.tools import DuckDuckGoSearchRun
                search = DuckDuckGoSearchRun()
                return search.run(query)
            except:
                return "搜索工具不可用"

        def calculator(expr):
            try:
                return str(eval(expr))
            except:
                return "计算错误，请输入合法表达式"

        return {
            "WebSearch": web_search,
            "Calculator": calculator
        }

    def _get_system_prompt(self):
        tools_desc = "\n".join([f"- {name}: {func.__doc__ if func.__doc__ else '无描述'}" 
                              for name, func in self.tools.items()])
        
        return f"""
你是一名专业的学习助手智能体。

可用工具：
{tools_desc}

规则：
1. 如果需要使用工具，输出JSON格式：{{"tool":"工具名称","args":"参数"}}
2. 如果不需要工具，直接回答问题
3. 回答要简洁、清晰
"""

    def _call_tool(self, tool_name, args):
        if tool_name in self.tools:
            return self.tools[tool_name](args)
        return f"未知工具: {tool_name}"

    def chat(self, user_input: str) -> str:
        self.chat_history.append({"role": "user", "content": user_input})
        
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.chat_history)
        
        response = self.client.chat.completions.create(
            model='qwen3-max',
            messages=messages,
            temperature=0.3,
            max_tokens=1024
        )
        
        content = response.choices[0].message.content
        
        try:
            tool_call = json.loads(content)
            if "tool" in tool_call and "args" in tool_call:
                result = self._call_tool(tool_call["tool"], tool_call["args"])
                self.chat_history.append({"role": "assistant", "content": content})
                self.chat_history.append({"role": "user", "content": f"工具返回: {result}"})
                
                messages = [{"role": "system", "content": "将工具结果用自然语言总结给用户"}]
                messages.extend(self.chat_history)
                
                final_response = self.client.chat.completions.create(
                    model='qwen3-max',
                    messages=messages,
                    temperature=0.3,
                    max_tokens=1024
                )
                content = final_response.choices[0].message.content
        except json.JSONDecodeError:
            pass
        
        self.chat_history.append({"role": "assistant", "content": content})
        return content