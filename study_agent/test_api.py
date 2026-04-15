import requests
import json

try:
    r = requests.post('http://127.0.0.1:5000/api/chat', json={'message': '什么是Python?'})
    print('Status:', r.status_code)
    print('Response:', r.text)
    
    with open('api_test_result.txt', 'w', encoding='utf-8') as f:
        f.write(f'Status: {r.status_code}\n')
        f.write(f'Response: {r.text}\n')
        
    print('Result saved to api_test_result.txt')
    
except Exception as e:
    print('Error:', str(e))
    with open('api_test_result.txt', 'w', encoding='utf-8') as f:
        f.write(f'Error: {str(e)}\n')