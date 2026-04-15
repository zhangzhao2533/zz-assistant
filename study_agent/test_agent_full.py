import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('Step 1: Importing StudyAgent...')
try:
    from core.agent import StudyAgent
    print('Step 1a: Import successful')
except Exception as e:
    print(f'Step 1a: Import failed: {str(e)}')
    import traceback
    print(f'Traceback: {traceback.format_exc()}')
    sys.exit(1)

print('Step 2: Creating agent...')
try:
    agent = StudyAgent()
    print('Step 2a: Agent created successfully')
except Exception as e:
    print(f'Step 2a: Agent creation failed: {str(e)}')
    import traceback
    print(f'Traceback: {traceback.format_exc()}')
    sys.exit(1)

print('Step 3: Testing chat...')
try:
    reply = agent.chat('Hello')
    print(f'Step 3a: Chat successful')
    print(f'Reply: {reply}')
except Exception as e:
    print(f'Step 3a: Chat failed: {str(e)}')
    import traceback
    print(f'Traceback: {traceback.format_exc()}')
    sys.exit(1)