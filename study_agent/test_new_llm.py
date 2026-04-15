import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('DASHSCOPE_API_KEY')
print('API Key:', key[:10] + '...')

try:
    from openai import OpenAI
    print('OpenAI imported')
    
    client = OpenAI(
        api_key=key,
        base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
    )
    print('Client created')
    
    response = client.chat.completions.create(
        model='qwen3-max',
        messages=[{'role': 'user', 'content': 'Hello'}]
    )
    print('Response received')
    
    content = response.choices[0].message.content
    print('Content length:', len(content))
    
    f = open('result.txt', 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('Result saved to result.txt')
    
except Exception as e:
    print('Error:', str(e))
    import traceback
    f = open('error.txt', 'w', encoding='utf-8')
    f.write(str(e) + '\n' + traceback.format_exc())
    f.close()
    print('Error saved to error.txt')