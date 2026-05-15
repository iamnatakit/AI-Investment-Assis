import streamlit as st
import requests
import time

API_URL = "http://localhost:8001/chat"

st.set_page_config(page_title="Baseline Investment AI", layout="wide")
st.title("📈 Project 1: Investment AI Agent (Baseline)")
st.write("ระบบพื้นฐาน: ใช้ Single LLM และ Large Prompt สำหรับจัดการคำถามด้านการลงทุน")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("สอบถามเกี่ยวกับการลงทุน..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send request to FastAPI backend
    with st.spinner("AI is thinking (Baseline)..."):
        try:
            response = requests.post(API_URL, json={"message": prompt})
            if response.status_code == 200:
                data = response.json()
                reply = data["reply"]
                metrics = f"⏱️ Latency: {data['latency_seconds']:.2f}s | 🪙 Tokens: {data['tokens_used']} | 💸 Cost: ${data['cost']:.5f}"
                
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    st.caption(metrics)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error("Error from API")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
