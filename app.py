import streamlit as st
import google.generativeai as genai

# --- 1. 配置与登录 ---
ACCESS_PASSWORD = "900802" 
st.set_page_config(page_title="蓝调 AI 实验室", page_icon="🎷", layout="wide")

if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 芝加哥蓝调：频道主理人后台")
    pwd = st.text_input("请输入访问密码", type="password")
    if st.button("登录"):
        if pwd == ACCESS_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
    st.stop()

# --- 2. 核心生成逻辑 ---
def get_ai_response(api_key, prompt):
    genai.configure(api_key=api_key)
    # 使用你最新的 3.1 模型
    model = genai.GenerativeModel('gemini-3.1-flash-lite')
    response = model.generate_content(prompt)
    return response.text

# --- 3. 界面布局 ---
st.title("🎷 蓝调自动化生成矩阵 (3.1 版)")

with st.sidebar:
    st.header("⚙️ 系统控制")
    api_key = st.text_input("Gemini API Key", type="password")
    if st.button("刷新素材"): st.rerun()
    
    try:
        with open("titles.txt", "r", encoding="utf-8") as f: titles = f.read()
        with open("comments.txt", "r", encoding="utf-8") as f: comments = f.read()
    except:
        titles, comments = "", ""
    st.info(f"记忆库: {len(titles.splitlines())} 标题 | {len(comments.splitlines())} 评论")

num_sets = st.slider("生成组数", 1, 10, 5)

if st.button("🚀 启动 3.1 模型生成"):
    if not api_key:
        st.error("请输入 API Key")
    else:
        prompt = f"""
        你是一位资深蓝调频道主理人。请参考以下素材生成 {num_sets} 组内容方案。
        参考爆款标题：{titles}
        参考观众评论：{comments}
        
        【要求】
        1. 保持：深夜、威士忌、孤独、芝加哥慢蓝调基调。
        2. 产出：Suno提示词(Eng)、YouTube标题(Cn)、Midjourney提示词(Eng)、互动话术。
        """
        with st.spinner("正在调用 Gemini 3.1 进行深度创作..."):
            result = get_ai_response(api_key, prompt)
            st.markdown(result)
            st.download_button("下载方案", result, "blues_plan.md")
