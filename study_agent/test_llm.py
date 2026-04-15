import sys
import os
from dotenv import load_dotenv

print('Step 1: Loading environment', flush=True)
sys.stdout.flush()

load_dotenv()
key = os.getenv('DASHSCOPE_API_KEY')
print(f'Step 2: API Key loaded: {key[:10]}...', flush=True)
sys.stdout.flush()

try:
    print('Step 3: Importing ChatOpenAI', flush=True)
    sys.stdout.flush()
    
    try:
        from langchain_openai import ChatOpenAI
        print('Step 3a: Import succeeded', flush=True)
        sys.stdout.flush()
    except Exception as import_err:
        print(f'Step 3a: Import failed: {str(import_err)}', flush=True)
        sys.stdout.flush()
        raise
    
    print('Step 4: Creating LLM instance', flush=True)
    sys.stdout.flush()
    
    llm = ChatOpenAI(
        model='qwen3-max',
        openai_api_key=key,
        openai_api_base='https://dashscope.aliyuncs.com/compatible-mode/v1',
        temperature=0.3,
        max_tokens=1024
    )
    
    print('Step 5: LLM created successfully', flush=True)
    sys.stdout.flush()
    
    print('Step 6: Invoking LLM', flush=True)
    sys.stdout.flush()
    
    result = llm.invoke('Hello')
    
    print('Step 7: LLM response received', flush=True)
    sys.stdout.flush()
    
    print(f'Result: {result.content}', flush=True)
    sys.stdout.flush()
    
except Exception as e:
    print(f'Error: {str(e)}', flush=True)
    import traceback
    print(f'Traceback: {traceback.format_exc()}', flush=True)
    sys.stdout.flush()