from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

def get_tools() -> list[Tool]:
    search = DuckDuckGoSearchRun()

    def simple_calculator(expr: str) -> str:
        try:
            return str(eval(expr))
        except:
            return "计算错误，请输入合法表达式"

    tools = [
        Tool(
            name="WebSearch",
            func=search.run,
            description="用于搜索知识点、最新信息、概念解释"
        ),
        Tool(
            name="Calculator",
            func=simple_calculator,
            description="用于数学计算：加减乘除、表达式"
        )
    ]
    return tools