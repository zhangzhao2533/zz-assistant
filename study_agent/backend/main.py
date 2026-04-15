import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.agent import StudyAgent

def main():
    print("=== 学习助手智能体（输入 exit 退出）===")
    agent = StudyAgent()

    while True:
        try:
            user_input = input("你：").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("智能体：再见！")
                break
            reply = agent.chat(user_input)
            print(f"智能体：{reply}\n")
        except UnicodeEncodeError:
            print("智能体：抱歉，输出包含特殊字符")
        except Exception as e:
            print(f"智能体：发生错误: {str(e)}")

if __name__ == "__main__":
    main()