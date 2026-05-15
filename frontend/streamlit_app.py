import streamlit as st

st.set_page_config(
    page_title="AI Agent Optimization Research",
    page_icon="📈",
    layout="wide"
)

st.title("AI Investment Agent Research")
st.write("""
Welcome to the Token Optimization Research UI.
This application allows you to compare two different AI agent architectures side-by-side:

1. **Project 1: Investment AI Agent (Baseline)**
   Uses a monolithic prompt and static large models for every query.

2. **Project 2: Investment AI Agent Intent (Optimized)**
   Uses an Intent Classifier, dynamic OpenRouter model routing, and specialized Google ADK Agents to drastically reduce costs.

Use the sidebar to navigate between the Chat interface and the analytics dashboards.
""")
