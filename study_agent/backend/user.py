import smtplib
from email.mime.text import MIMEText
from email.header import Header
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import time
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

user_bp = Blueprint('user', __name__)

users = {}
verification_codes = {}

try:
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)
except:
    users = {}

def save_users():
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False)

def send_verification_code(email):
    from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD
    
    code = ''.join([str(i) for i in range(1000, 10000)][0])
    import random
    code = ''.join(random.sample('0123456789', 4))
    
    verification_codes[email] = {
        'code': code,
        'expire_time': time.time() + 300
    }
    
    subject = '学习助手智能体 - 注册验证码'
    body = f'您的注册验证码是：{code}，有效期5分钟。'
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = MAIL_USERNAME
    msg['To'] = email
    
    try:
        server = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, [email], msg.as_string())
        server.quit()
        return True, code
    except Exception as e:
        return False, str(e)

@user_bp.route('/api/send_code', methods=['POST'])
def send_code():
    try:
        data = request.get_json()
        email = data.get('qq_email')
        
        if not email or not email.endswith('@qq.com'):
            return jsonify({"success": False, "message": "请输入有效的QQ邮箱"}), 400
        
        if email in users:
            return jsonify({"success": False, "message": "该邮箱已注册"}), 400
        
        success, info = send_verification_code(email)
        
        if success:
            return jsonify({"success": True, "message": "验证码已发送，请查收邮箱"})
        else:
            return jsonify({"success": False, "message": f"发送失败：{info}"}), 500
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('qq_email')
        password = data.get('password')
        code = data.get('code')
        
        if not email or not email.endswith('@qq.com'):
            return jsonify({"success": False, "message": "请输入有效的QQ邮箱"}), 400
        
        if not password or len(password) < 6:
            return jsonify({"success": False, "message": "密码长度至少6位"}), 400
        
        if not code or len(code) != 4:
            return jsonify({"success": False, "message": "请输入4位验证码"}), 400
        
        if email in users:
            return jsonify({"success": False, "message": "该邮箱已注册"}), 400
        
        if email not in verification_codes:
            return jsonify({"success": False, "message": "请先获取验证码"}), 400
        
        if time.time() > verification_codes[email]['expire_time']:
            return jsonify({"success": False, "message": "验证码已过期，请重新获取"}), 400
        
        if verification_codes[email]['code'] != code:
            return jsonify({"success": False, "message": "验证码错误"}), 400
        
        hashed_password = generate_password_hash(password)
        users[email] = {
            'password': hashed_password,
            'created_at': time.time()
        }
        save_users()
        
        del verification_codes[email]
        
        return jsonify({"success": True, "message": "注册成功，请登录"})
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('qq_email')
        password = data.get('password')
        
        if not email or not email.endswith('@qq.com'):
            return jsonify({"success": False, "message": "请输入有效的QQ邮箱"}), 400
        
        if not password:
            return jsonify({"success": False, "message": "请输入密码"}), 400
        
        if email not in users:
            return jsonify({"success": False, "message": "该邮箱未注册"}), 400
        
        if not check_password_hash(users[email]['password'], password):
            return jsonify({"success": False, "message": "密码错误"}), 400
        
        import uuid
        token = str(uuid.uuid4())
        
        if 'tokens' not in users[email]:
            users[email]['tokens'] = []
        users[email]['tokens'].append(token)
        save_users()
        
        return jsonify({
            "success": True, 
            "message": "登录成功",
            "token": token,
            "email": email
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/api/verify_token', methods=['POST'])
def verify_token():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({"success": False, "message": "缺少token"}), 400
        
        for email, user_data in users.items():
            if 'tokens' in user_data and token in user_data['tokens']:
                return jsonify({"success": True, "email": email})
        
        return jsonify({"success": False, "message": "无效的token"}), 401
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@user_bp.route('/api/logout', methods=['POST'])
def logout():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({"success": False, "message": "缺少token"}), 400
        
        for email, user_data in users.items():
            if 'tokens' in user_data and token in user_data['tokens']:
                user_data['tokens'].remove(token)
                save_users()
                return jsonify({"success": True, "message": "退出成功"})
        
        return jsonify({"success": False, "message": "无效的token"}), 401
        
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500