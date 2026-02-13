import streamlit as st
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="GSI AMER Dashboard - Suneel", layout="wide")
st.title("🚀 GSI Americas Dashboard")
st.markdown("**Real-time Pipeline | Cadence Tracker | $5M P&L Simulator**")

# ========================== SECRETS ==========================
if "sf" not in st.session_state:
    try:
        sf = Salesforce(
            username=st.secrets["salesforce"]["username"],
            password=st.secrets["salesforce"]["password"],
            security_token=st.secrets["salesforce"]["security_token"]
        )
        st.session_state.sf = sf
        st.success("✅ Connected to Salesforce")
    except Exception as e:
        st.error("Salesforce connection failed. Check secrets.toml")
        st.stop()

sf = st.session_state.sf

# ========================== DATA ==========================
query = """
SELECT Id, Name, Amount, StageName, CloseDate, GSI_Partner__c 
FROM Opportunity 
WHERE GSI_Partner__c != null 
ORDER BY CloseDate DESC
"""
result = sf.query(query)
df = pd.DataFrame(result['records'])

# ========================== DASHBOARD ==========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pipeline", f"${df['Amount'].sum():,.0f}")
col2.metric("Active Opportunities", len(df))
col3.metric("Avg Deal Size", f"${df['Amount'].mean():,.0f}")
col4.metric("Win Rate Target", "30%")

# Pipeline Gauge
st.subheader("Pipeline vs $15M Year-1 Target")
fig, ax = plt.subplots(figsize=(6, 3))
ax.barh(['Current'], [df['Amount'].sum()], color='#00B336')
ax.barh(['Target'], [15000000], color='#1E3A5F', alpha=0.3)
ax.set_xlim(0, 20000000)
st.pyplot(fig)

# Cadence Tracker
st.subheader("Weekly Cadence Tracker")
cadence = {
    "MEDDICC Reviews Completed": 12,
    "Workshops Delivered": 8,
    "EBC/QBRs Held": 5,
    "Attach Rate Achieved": "58%"
}
st.bar_chart(cadence)

# P&L Simulator
st.subheader("What-If P&L Simulator")
mindshare = st.slider("Mindshare Uplift % (from workshops & enablement)", 0, 60, 30)
pnl = 5000000 * (1 + mindshare/100)
st.metric("Projected Year-1 GSI P&L", f"${pnl:,.0f}", delta=f"+${pnl-5000000:,.0f}")
