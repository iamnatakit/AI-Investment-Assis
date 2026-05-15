import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db_utils import load_table

st.set_page_config(page_title="Project Comparison", page_icon="⚖️", layout="wide")
st.title("Baseline vs Optimized Comparison")

df_usage = load_table("usage_logs")

if df_usage.empty:
    st.info("No data available for comparison. Connect the database and make chat requests on BOTH projects.")
else:
    baseline = df_usage[df_usage['project_name'] == 'project_1_baseline']
    optimized = df_usage[df_usage['project_name'] == 'project_2_intent']
    
    if baseline.empty or optimized.empty:
        st.warning("Need data from BOTH projects to show full comparative efficiency gains.")
    
    b_tokens = baseline['total_tokens'].sum() if not baseline.empty else 0
    o_tokens = optimized['total_tokens'].sum() if not optimized.empty else 0
    b_cost = baseline['cost_usd'].sum() if not baseline.empty else 0
    o_cost = optimized['cost_usd'].sum() if not optimized.empty else 0
    b_lat = baseline['latency_ms'].mean() if not baseline.empty else 0
    o_lat = optimized['latency_ms'].mean() if not optimized.empty else 0
    
    token_saving = ((b_tokens - o_tokens) / b_tokens * 100) if b_tokens > 0 else 0
    cost_saving = ((b_cost - o_cost) / b_cost * 100) if b_cost > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Project 1 (Baseline)")
        st.metric("Avg Latency", f"{b_lat:.0f} ms")
        st.metric("Total Tokens", b_tokens)
        st.metric("Total Cost", f"${b_cost:.4f}")
        
    with col2:
        st.subheader("Project 2 (Optimized)")
        st.metric("Avg Latency", f"{o_lat:.0f} ms", delta=f"{o_lat - b_lat:.0f} ms", delta_color="inverse")
        st.metric("Total Tokens", o_tokens, delta=f"{o_tokens - b_tokens}", delta_color="inverse")
        st.metric("Total Cost", f"${o_cost:.4f}", delta=f"${o_cost - b_cost:.4f}", delta_color="inverse")

    st.divider()
    st.subheader("Efficiency Gains")
    col3, col4 = st.columns(2)
    col3.metric("Token Saving %", f"{token_saving:.1f}%")
    col4.metric("Cost Saving %", f"{cost_saving:.1f}%")
