import streamlit as st
import requests
import time

API_URL = "http://localhost:8002/chat"

st.set_page_config(page_title="Optimized Investment AI", layout="wide")
st.title("🚀 Project 2: Investment AI Agent Intent (Optimized)")
st.write("ระบบประสิทธิภาพสูง: ใช้ Intent Classifier, OpenRouter, Google ADK Multi-Agent และ Monitor")

# Sidebar for Monitoring
with st.sidebar:
    st.header("📊 System Monitoring")
    st.metric("Total Tokens (Session)", "0")
    st.metric("Total Cost (Session)", "$0.0000")
    st.write("### Billing History")
    st.info("No billing data yet.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("สอบถามข้อมูลการลงทุน, หุ้น หรือผลตอบแทน..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Send request to FastAPI backend
    with st.spinner("Multi-Agent Orchestrating Task..."):
        try:
            response = requests.post(API_URL, json={"message": prompt})
            if response.status_code == 200:
                data = response.json()
                reply = data["reply"]
                intent = data["intent_detected"]
                agents = ", ".join(data["agents_used"])
                
                # Metrics string
                metrics = f"🎯 Intent: {intent} | 🤖 Agents: {agents}\n⏱️ Latency: {data['latency_seconds']:.2f}s | 🪙 Tokens: {data['tokens_used']} | 💸 Cost: ${data['cost']:.5f}"
                
                with st.chat_message("assistant"):
                    st.markdown(reply)
                    st.caption(metrics)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": reply})
            else:
                st.error("Error from API")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
