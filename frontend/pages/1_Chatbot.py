import streamlit as st
import requests
import uuid
import os

st.set_page_config(page_title="Chatbot Interface", page_icon="💬")

st.title("Investment Chatbot")

# Settings
project_choice = st.radio("Select Project Architecture:", 
                          ["Project 1: Baseline", "Project 2: Intent Optimized"])

user_id = st.text_input("User ID", value="demo_user")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
session_id = st.text_input("Session ID", value=st.session_state.session_id)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "metadata" in msg:
            with st.expander("View Request Metadata"):
                st.json(msg["metadata"])

if prompt := st.chat_input("Ask for investment advice..."):
    # Add user msg
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine endpoint dynamically based on project
    if project_choice == "Project 1: Baseline":
        base_url = os.environ.get("BACKEND_URL_P1", "http://localhost:8001")
        endpoint = f"{base_url}/investment-ai-agent/chat"
    else:
        base_url = os.environ.get("BACKEND_URL_P2", "http://localhost:8002")
        endpoint = f"{base_url}/investment-ai-agent-intent/chat"

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(endpoint, json={
                    "user_id": user_id,
                    "session_id": session_id,
                    "message": prompt
                })
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", data.get("message", "No content"))
                    st.markdown(answer)
                    
                    # Store metadata
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "metadata": data
                    })
                    
                    with st.expander("View Request Metadata", expanded=True):
                        st.json(data)
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {str(e)}\n\nMake sure Project 1 is on port 8001 and Project 2 is on port 8002.")
