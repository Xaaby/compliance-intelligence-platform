"""
compliance-intelligence-platform
Single Streamlit app — three navbar tabs — calls all three agent backends.
Entry point for Cloud Run deployment.
"""
import streamlit as st
from tabs import tab_devops, tab_ccai, tab_gov

st.set_page_config(
    page_title="Compliance Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🛡️ Compliance Intelligence Platform")
st.caption(
    "Three AI agents. One architecture. "
    "Infrastructure compliance · Contact center QA · Government intelligence."
)
st.divider()

tab1, tab2, tab3 = st.tabs([
    "🔧 DevOps Compliance",
    "📞 Contact Center QA",
    "🏛️ Government Intelligence"
])

with tab1:
    tab_devops.render()

with tab2:
    tab_ccai.render()

with tab3:
    tab_gov.render()
