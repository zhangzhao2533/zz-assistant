import sys
import os
from dotenv import load_dotenv

load_dotenv()

client = None
try:
    from openai import OpenAI
    print('OpenAI imported', flush=True)
    
    client = OpenAI(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
    )
    print('Client created', flush=True)
    
    response = client.chat.completions.create(
        model='qwen3-max',
        messages=[{'role': 'user', 'content': 'Hello'}]
    )
    print('Response received', flush=True)
    print(f'Result: {response.choices[0].message.content}', flush=True)
    
except Exception as e:
    print(f'Error: {str(e)}', flush=True)
    import traceback
    print(f'Traceback: {traceback.format_exc()}', flush=True)