import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db_utils import load_table

st.set_page_config(page_title="Chat History", page_icon="📜", layout="wide")
st.title("Chat History")

df_chat = load_table("chat_messages")

if df_chat.empty:
    st.info("No chat history available. Connect the database and make some chat requests!")
else:
    sessions = df_chat['session_id'].unique()
    selected_session = st.selectbox("Select Session ID", sessions)
    
    session_data = df_chat[df_chat['session_id'] == selected_session].sort_values('created_at')
    
    for _, row in session_data.iterrows():
        with st.chat_message(row['role']):
            st.markdown(row['content'])
            st.caption(f"Project: {row['project_name']} | Time: {row['created_at']}")
            
    st.subheader("Raw Chat Data")
    st.dataframe(df_chat)
