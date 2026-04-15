import streamlit as st
import requests
import json

st.set_page_config(page_title="学习助手智能体", page_icon="📚", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = 'login'
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def show_login():
    st.title("🔐 登录")
    
    with st.form("login_form"):
        email = st.text_input("QQ邮箱", placeholder="请输入QQ邮箱")
        password = st.text_input("密码", type="password", placeholder="请输入密码")
        submit = st.form_submit_button("登录")
        
        if submit:
            if not email.endswith('@qq.com'):
                st.error("请输入有效的QQ邮箱")
            elif not password:
                st.error("请输入密码")
            else:
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/api/login",
                        json={"qq_email": email, "password": password}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.session_state.user_info = {
                            "email": data["email"],
                            "token": data["token"]
                        }
                        st.session_state.page = 'chat'
                        st.rerun()
                    else:
                        st.error(data.get("message", "登录失败"))
                except Exception as e:
                    st.error(f"连接失败: {str(e)}")
    
    if st.button("没有账号？去注册"):
        st.session_state.page = 'register'
        st.rerun()

def show_register():
    st.title("📝 注册")
    
    with st.form("register_form"):
        email = st.text_input("QQ邮箱", placeholder="请输入QQ邮箱")
        password = st.text_input("密码", type="password", placeholder="密码长度至少6位")
        confirm_password = st.text_input("确认密码", type="password", placeholder="请再次输入密码")
        code = st.text_input("验证码", placeholder="请输入4位验证码")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            get_code = st.form_submit_button("获取验证码")
        with col2:
            submit = st.form_submit_button("注册")
        
        if get_code:
            if not email.endswith('@qq.com'):
                st.error("请输入有效的QQ邮箱")
            else:
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/api/send_code",
                        json={"qq_email": email}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("验证码已发送，请查收邮箱")
                    else:
                        st.error(data.get("message", "发送失败"))
                except Exception as e:
                    st.error(f"连接失败: {str(e)}")
        
        if submit:
            if not email.endswith('@qq.com'):
                st.error("请输入有效的QQ邮箱")
            elif len(password) < 6:
                st.error("密码长度至少6位")
            elif password != confirm_password:
                st.error("两次输入的密码不一致")
            elif len(code) != 4:
                st.error("请输入4位验证码")
            else:
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/api/register",
                        json={"qq_email": email, "password": password, "code": code}
                    )
                    data = response.json()
                    
                    if data.get("success"):
                        st.success("注册成功，请登录")
                        st.session_state.page = 'login'
                        st.rerun()
                    else:
                        st.error(data.get("message", "注册失败"))
                except Exception as e:
                    st.error(f"连接失败: {str(e)}")
    
    if st.button("已有账号？去登录"):
        st.session_state.page = 'login'
        st.rerun()

def show_chat():
    st.title("📚 学习助手智能体")
    
    st.sidebar.write(f"当前用户: {st.session_state.user_info['email']}")
    if st.sidebar.button("退出登录"):
        try:
            requests.post(
                "http://127.0.0.1:5000/api/logout",
                json={"token": st.session_state.user_info['token']}
            )
        except:
            pass
        st.session_state.user_info = None
        st.session_state.chat_history = []
        st.session_state.page = 'login'
        st.rerun()
    
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant"):
                st.write(message["content"])
    
    user_input = st.chat_input("输入问题:")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        try:
            response = requests.post(
                "http://127.0.0.1:5000/api/chat",
                json={"message": user_input}
            )
            data = response.json()
            reply = data.get("reply", "暂无回复")
        except Exception as e:
            reply = f"连接失败: {str(e)}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

if st.session_state.page == 'login':
    show_login()
elif st.session_state.page == 'register':
    show_register()
elif st.session_state.page == 'chat':
    show_chat()