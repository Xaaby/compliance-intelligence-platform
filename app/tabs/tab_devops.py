"""
Tab 1: DevOps Compliance Agent UI.
Calls Agent 1 backend via agent1_client.
"""
import streamlit as st
from app.api_clients.agent1_client import chat, health_check

SAMPLE_QUERIES = [
    "Why did my pipeline fail last night?",
    "Is my pipeline SOC 2 compliant this week?",
    "Give me a full audit report for the last 7 days.",
    "What were the IAM violations in the last 7 days?",
    "Show me all failed Cloud Functions runs in the last 24 hours."
]


def render():
    st.subheader("🔧 GCP DevOps Compliance Agent")
    st.caption("Monitors GCP pipelines for SOC 2 and NIST compliance violations.")

    try:
        h = health_check()
        st.success("Agent online", icon="🟢")
    except Exception:
        st.error("Agent offline — check backend URL", icon="🔴")
        return

    st.divider()

    selected = st.selectbox(
        "Select a sample query or type your own:",
        ["— type your own —"] + SAMPLE_QUERIES
    )
    query = st.text_area(
        "Query",
        value="" if selected == "— type your own —" else selected,
        height=80,
        placeholder="Ask about pipeline health, compliance status, or audit reports..."
    )

    if st.button("Run Query", type="primary", key="agent1_run"):
        if not query.strip():
            st.warning("Enter a query first.")
            return
        with st.spinner("Agent thinking..."):
            try:
                result = chat(query)
                st.markdown("### Agent Response")
                st.markdown(result.get("response", "No response."))
                if result.get("tools_called"):
                    st.caption(f"Tools used: {', '.join(result['tools_called'])}")
            except Exception as e:
                st.error(f"Request failed: {e}")
