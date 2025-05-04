from dotenv import load_dotenv
load_dotenv()


import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# --- LLMインスタンス ---
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# --- 専門家選択に応じたシステムプロンプトを生成 ---
def get_system_prompt(expert_type):
    if expert_type == "A":
        return "あなたは睡眠アドバイザーです。睡眠に悩みを抱えている人に対して適切なアドバイスをしてあげてください"
    elif expert_type == "B":
        return "あなたはダイエットアドバイザーです。老化を防止するためにいい食べ物、悪い食べ物のアドバイスをしてください"
    else:
        return "あなたは親切なアドバイザーです。"

# --- 入力テキストと選択値を受けてLLMの応答を取得 ---
def get_llm_response(user_input, expert_type):
    messages = [
        SystemMessage(content=get_system_prompt(expert_type)),
        HumanMessage(content=user_input)
    ]
    result = llm(messages)
    return result.content

# --- Streamlit アプリ構成 ---
st.set_page_config(page_title="専門家AIアドバイザー", layout="centered")
st.title("🧠 専門家AIアドバイザー")

st.markdown("""
このWebアプリでは、次の2種類の専門家AIに相談することができます：

- **A：睡眠アドバイザー** — 睡眠に関する悩みやアドバイスを提供します。
- **B：ダイエットアドバイザー** — 老化防止を目的とした食生活のアドバイスを行います。

下記のフォームから質問を入力し、相談したい専門家を選んでください。
""")

# --- ユーザー入力フォーム ---
st.markdown("### 相談フォーム")
if "responses" not in st.session_state:
    st.session_state.responses = []  # 過去のアドバイスを保存

with st.form(key="consult_form"):
    user_input = st.text_area("あなたの相談内容を入力してください：", height=150)
    expert_choice = st.radio("相談したい専門家を選んでください：", ["A（睡眠アドバイザー）", "B（ダイエットアドバイザー）"])
    submit = st.form_submit_button("相談する")

# 入力が送信されたら処理
if submit:
    if not user_input.strip():
        st.warning("相談内容を入力してください。")
    else:
        expert_type = "A" if expert_choice.startswith("A") else "B"
        with st.spinner("AIが回答を作成中です..."):
            response = get_llm_response(user_input, expert_type)
        st.session_state.responses.append({"input": user_input, "response": response})
        st.success("AIからのアドバイスを取得しました！")

# 過去のアドバイスを表示
if st.session_state.responses:
    st.markdown("### 過去の相談とアドバイス")
    for i, entry in enumerate(st.session_state.responses, 1):
        st.markdown(f"**相談 {i}:** {entry['input']}")
        st.markdown(f"**アドバイス {i}:** {entry['response']}")
        st.markdown("---")
