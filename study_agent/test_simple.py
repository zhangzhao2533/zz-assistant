import sys
print('Test 1: Basic print', flush=True)
sys.stdout.flush()

import os
print('Test 2: OS module loaded', flush=True)
sys.stdout.flush()

from dotenv import load_dotenv
print('Test 3: dotenv loaded', flush=True)
sys.stdout.flush()

load_dotenv()
key = os.getenv('DASHSCOPE_API_KEY')
print(f'Test 4: API Key exists: {key is not None}', flush=True)
sys.stdout.flush()

print('Done!', flush=True)
sys.stdout.flush()