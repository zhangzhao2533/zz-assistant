from core.agent import StudyAgent

agent = StudyAgent()

output_lines = []

output_lines.append("=== 测试学习助手智能体 ===")

output_lines.append("\n测试1: 直接回答问题")
reply = agent.chat("什么是Python?")
output_lines.append(f"智能体：{reply}")

output_lines.append("\n测试2: 计算")
reply = agent.chat("计算 (25+5)*3/2")
output_lines.append(f"智能体：{reply}")

output_lines.append("\n测试3: 使用搜索")
reply = agent.chat("2025年AI最新进展")
output_lines.append(f"智能体：{reply}")

output_lines.append("\n测试完成！")

with open("final_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
    
print("Results saved to final_output.txt")