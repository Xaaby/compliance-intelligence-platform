"""
Tab 3: Government Citizen Intelligence Platform UI.
Two sub-modes: 311 Classifier and CJIS Policy Q&A.
Calls Agent 3 backend via agent3_client.
"""
import streamlit as st
from api_clients.agent3_client import classify_request, query_cjis, health_check

SAMPLE_COMPLAINTS = {
    "REQ-001": {
        "label": "REQ-001 — Single issue (pothole)",
        "text": "There is a large pothole on Oak Street near the intersection with 5th Avenue. It has been there for six months and has damaged my tire twice."
    },
    "REQ-002": {
        "label": "REQ-002 — Two departments (fallen tree + streetlight)",
        "text": "A tree fell on Maple Drive last night during the storm and it knocked out the streetlight at the corner. The road is partially blocked and it is dark and dangerous."
    },
    "REQ-003": {
        "label": "REQ-003 — CRITICAL (water main burst)",
        "text": "There is a water main burst at the corner of Pine and 3rd. Water is flooding the street and going into nearby basements. This just started an hour ago and is getting worse."
    },
    "REQ-004": {
        "label": "REQ-004 — Low urgency (abandoned car + graffiti)",
        "text": "There is an abandoned car on Cedar Lane that has been there for two weeks with no plates. Also there is graffiti on the wall of the building next to it."
    },
    "REQ-005": {
        "label": "REQ-005 — Complex multi-issue (5 departments)",
        "text": "On Riverside Boulevard there is a pothole that damaged my car, a broken streetlight making it dangerous at night, a flooded storm drain blocking traffic, an abandoned vehicle in the bike lane, and someone has been illegally dumping trash behind the bus stop for the past week."
    }
}

SAMPLE_CJIS_QUESTIONS = {
    "Q-001": "What encryption standard does CJIS require for data at rest on mobile devices?",
    "Q-002": "How often must agencies conduct security awareness training under CJIS?",
    "Q-003": "What are the CJIS requirements for multi-factor authentication?",
    "Q-004": "Can cloud service providers store Criminal Justice Information under CJIS?",
    "Q-005": "What does CJIS require for incident response planning?"
}

URGENCY_COLORS = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢"
}


@st.cache_data(ttl=60, show_spinner=False)
def _cached_health_check() -> dict | None:
    try:
        return health_check()
    except Exception:
        return None


def render():
    st.subheader("🏛️ Government Citizen Intelligence Platform")
    st.caption("311 citizen request classifier + CJIS Security Policy Q&A.")

    health = _cached_health_check()
    if health is None:
        st.warning(
            "Backend unreachable — requests may still work if the service is warming up. "
            "First cold start can take up to 90 seconds while the CJIS index loads.",
            icon="⚠️",
        )
    elif health.get("index_loaded"):
        st.success("Agent online — CJIS index loaded", icon="✅")
    else:
        st.info("Agent online — CJIS index still loading, first Q&A query may be slow", icon="ℹ️")

    st.divider()

    mode = st.radio(
        "Select mode:",
        ["🏙️ 311 Citizen Request Classifier", "📋 CJIS Policy Q&A"],
        horizontal=True,
        key="gov_mode"
    )

    if mode == "🏙️ 311 Citizen Request Classifier":
        selected_req = st.selectbox(
            "Select a sample complaint or type your own:",
            ["— type your own —"] + list(SAMPLE_COMPLAINTS.keys()),
            format_func=lambda k: SAMPLE_COMPLAINTS[k]["label"] if k != "— type your own —" else k
        )
        complaint_text = st.text_area(
            "Complaint text:",
            value="" if selected_req == "— type your own —" else SAMPLE_COMPLAINTS[selected_req]["text"],
            height=120
        )
        request_id = selected_req if selected_req != "— type your own —" else "REQ-CUSTOM"

        if st.button("Classify Request", type="primary", key="classify_run"):
            if not complaint_text.strip():
                st.warning("Enter a complaint first.")
                return
            with st.spinner("Classifying..."):
                try:
                    result = classify_request(request_id, complaint_text)
                except Exception as e:
                    st.error(f"Request failed: {e}")
                    return

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("#### Classification")
                urgency = result.get("urgency", "")
                icon = URGENCY_COLORS.get(urgency, "⚪")
                st.metric("Primary Dept", result.get("primary_department", ""))
                st.metric("Urgency", f"{icon} {urgency}")
                st.metric("SLA", f"{result.get('sla_hours', '')} hours")
                st.caption(f"Confidence: {result.get('classification_confidence', '')}")

            with col2:
                st.markdown("#### Work Orders")
                for wo in result.get("work_orders", []):
                    wo_icon = URGENCY_COLORS.get(wo.get("urgency", ""), "⚪")
                    st.markdown(f"**{wo_icon} {wo.get('department', '')}**")
                    st.caption(f"{wo.get('action_type', '')} — {wo.get('sla_hours', '')}hr SLA")
                    st.caption(wo.get("issue_description", ""))
                    st.divider()

            with col3:
                st.markdown("#### Acknowledgment Letter")
                st.info(result.get("acknowledgment_letter", ""))

    else:
        selected_q = st.selectbox(
            "Select a sample question or type your own:",
            ["— type your own —"] + list(SAMPLE_CJIS_QUESTIONS.keys()),
            format_func=lambda k: SAMPLE_CJIS_QUESTIONS[k][:80] + "..." if k != "— type your own —" else k
        )
        question = st.text_area(
            "CJIS policy question:",
            value="" if selected_q == "— type your own —" else SAMPLE_CJIS_QUESTIONS[selected_q],
            height=100,
            placeholder="What does CJIS require for..."
        )
        query_id = selected_q if selected_q != "— type your own —" else "Q-CUSTOM"

        if st.button("Search Policy", type="primary", key="cjis_run"):
            if not question.strip():
                st.warning("Enter a question first.")
                return
            with st.spinner("Searching CJIS policy..."):
                try:
                    result = query_cjis(query_id, question)
                except Exception as e:
                    st.error(f"Request failed: {e}")
                    return

            if result.get("cannot_answer"):
                st.warning(
                    "This question may be outside the scope of the CJIS Security Policy document, "
                    "or the retrieved sections do not contain enough information to answer reliably. "
                    "Consult your CJIS Systems Officer directly.",
                    icon="⚠️"
                )
                return

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown("#### Policy Answer")
                confidence = result.get("confidence", "")
                conf_icon = "🟢" if confidence == "HIGH" else "🟡" if confidence == "MEDIUM" else "🔴"
                st.caption(f"Confidence: {conf_icon} {confidence}")
                st.markdown(result.get("answer", ""))

            with col2:
                st.markdown("#### Citations")
                for citation in result.get("citations", []):
                    st.markdown(f"**📄 {citation.get('section_id', '')}**")
                    st.caption(citation.get("section_title", ""))
                    st.caption(f"_{citation.get('policy_version', '')}_")
                    st.caption(citation.get("relevance", ""))
                    st.divider()

        st.caption(
            "⚠️ This tool answers questions about the publicly available CJIS Security Policy document only. "
            "It does not process, store, or transmit actual Criminal Justice Information."
        )
