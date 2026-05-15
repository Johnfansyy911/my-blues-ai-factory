import streamlit as st
import google.generativeai as genai
import os

# --- 权限控制：设置你的访问密码 ---
ACCESS_PASSWORD = "你的自定义登录密码" 

# --- 基础配置 ---
st.set_page_config(page_title="蓝调 AI 实验室", page_icon="🎷")

# 登录逻辑
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    if st.session_state["pwd_input"] == ACCESS_PASSWORD:
        st.session_state["authenticated"] = True
    else:
        st.error("密码错误！")

if not st.session_state["authenticated"]:
    st.title("🔒 私人频道管理后台")
    st.text_input("请输入访问密码", type="password", key="pwd_input", on_change=check_password)
    st.stop() # 停止运行后续代码

# --- 登录后的主程序 ---
st.title("🎷 芝加哥蓝调：爆款学习型生成矩阵")

# 侧边栏 API 配置
with st.sidebar:
    st.header("核心配置")
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.header("深度学习")
    new_titles = st.text_area("输入新爆款标题")
    new_comments = st.text_area("输入新高赞评论")
    
    if st.button("喂养数据"):
        with open("titles.txt", "a") as f: f.write(new_titles + "\n")
        with open("comments.txt", "a") as f: f.write(new_comments + "\n")
        st.success("学习素材已更新")

# 生成逻辑 (引用之前给你的 Gemini 生成代码...)
if st.button("🚀 开始生成方案"):
    if not api_key:
        st.warning("请在侧边栏填入 API Key")
    else:
        # ... (这里放之前给你的 genai 生成逻辑代码)
        st.write("生成中...")
        # 简化版示例
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("请生成3组蓝调方案...")
        st.markdown(response.text)