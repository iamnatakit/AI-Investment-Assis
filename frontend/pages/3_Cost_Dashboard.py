import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db_utils import load_table

st.set_page_config(page_title="Cost Dashboard", page_icon="💵", layout="wide")
st.title("Cost Dashboard")

df_billing = load_table("billing_ledger")

if df_billing.empty:
    st.info("No billing data available. Connect the database and make some chat requests!")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost (USD)", f"${df_billing['cost_usd'].sum():.4f}")
    col2.metric("Total Cost (THB)", f"฿{df_billing['cost_thb'].sum():.4f}")
    col3.metric("Avg Cost / Request", f"${df_billing['cost_usd'].mean():.4f}")

    st.subheader("Cost by Project")
    cost_summary = df_billing.groupby('project_name')['cost_usd'].sum().reset_index()
    st.bar_chart(cost_summary.set_index('project_name'))
    
    st.subheader("Billing Ledger")
    st.dataframe(df_billing)
