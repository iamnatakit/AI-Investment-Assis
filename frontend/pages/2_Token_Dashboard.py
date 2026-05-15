import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db_utils import load_table

st.set_page_config(page_title="Token Dashboard", page_icon="🪙", layout="wide")
st.title("Token Usage Dashboard")

df_usage = load_table("usage_logs")

if df_usage.empty:
    st.info("No usage data available. Connect the database and make some chat requests!")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total API Requests", len(df_usage))
    col2.metric("Total Tokens Used", df_usage['total_tokens'].sum())
    col3.metric("Avg Tokens / Request", round(df_usage['total_tokens'].mean(), 2))

    st.subheader("Token Usage by Project")
    project_summary = df_usage.groupby('project_name')['total_tokens'].sum().reset_index()
    st.bar_chart(project_summary.set_index('project_name'))
    
    st.subheader("Raw Usage Logs")
    st.dataframe(df_usage)
