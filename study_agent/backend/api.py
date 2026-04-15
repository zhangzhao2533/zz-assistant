from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import io
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from core.agent import StudyAgent
from user import user_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_bp)

agent = StudyAgent()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if 'message' not in data:
            return jsonify({"error": "缺少message字段"}), 400
        
        message = data['message']
        reply = agent.chat(message)
        
        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)