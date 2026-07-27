"""
Tab 2: Contact Center Intelligence Suite UI.
Calls Agent 2 backend via agent2_client.
"""
import streamlit as st
from api_clients.agent2_client import analyze_transcript, health_check

SAMPLE_CALLS = {
    "CALL-001": {
        "label": "CALL-001 — Clean call (no violations)",
        "agent_id": "AGENT-042",
        "queue_name": "Billing Support",
        "transcript_text": """[00:00:02] Agent: Thank you for calling Horizon Communications. This call may be recorded for quality and training purposes. My name is Sarah, how can I assist you today?
[00:00:10] Customer: Hi Sarah, I'm calling about my bill. I was charged twice for my internet service this month and I'd like to get that sorted out.
[00:00:18] Agent: I completely understand how frustrating that must be — seeing a double charge is never something you want on your statement. Let me pull up your account right now. Can I get your account number or the phone number associated with the account?
[00:00:30] Customer: Sure, it's 214-555-0198.
[00:00:34] Agent: Perfect, thank you. I'm just pulling that up now — give me just a moment while I access your billing history.
[00:00:45] Agent: Okay, I can see your account here. And you're absolutely right — I do see two separate charges for internet service on the 3rd and the 5th of this month. The second charge appears to be a system error on our end. I sincerely apologize for that.
[00:01:01] Customer: Okay, so can you reverse the duplicate?
[00:01:04] Agent: Absolutely. I'm going to initiate a credit of $79.99 back to your account right now. This will appear on your next statement, but if you were charged to a credit card, it typically posts within 3 to 5 business days. I'll also flag your account so our billing team reviews it to make sure this doesn't happen again.
[00:01:25] Customer: That's great, thank you. Will I get a confirmation?
[00:01:28] Agent: Yes — you'll receive a confirmation email to the address on file within the next 30 minutes. Is there anything else I can help you with today?
[00:01:36] Customer: No, that covers it. Thanks Sarah, I appreciate how quickly you handled that.
[00:01:41] Agent: My pleasure! I'm glad we could get that resolved for you. Your case number for this credit is CR-20240315-8821. Don't hesitate to call back if you have any other questions. Have a wonderful day!
[00:01:52] Customer: You too, bye.
[00:01:54] Agent: Goodbye!""",
    },
    "CALL-002": {
        "label": "CALL-002 — PCI violation (card number spoken aloud)",
        "agent_id": "AGENT-017",
        "queue_name": "Payment Processing",
        "transcript_text": """[00:00:03] Agent: Thank you for calling Horizon Communications. This call may be recorded for quality and training purposes. My name is Marcus. How can I help you today?
[00:00:12] Customer: Hi Marcus. I need to make a payment on my account. I've been getting disconnection notices and I want to make sure this gets applied today.
[00:00:20] Agent: Of course, I can absolutely help you process that payment right now. Let me bring up your account. Can I get your account number?
[00:00:27] Customer: Yes, it's 7782940.
[00:00:31] Agent: Got it, thank you. I see the account here. Your current balance due is $234.87. Would you like to pay that in full today?
[00:00:40] Customer: Yes, the full amount. I'll use my Visa card.
[00:00:43] Agent: Great. Go ahead and give me your card number.
[00:00:46] Customer: It's 4532 1234 5678 9010.
[00:00:52] Agent: And the expiration date?
[00:00:54] Customer: 09/27.
[00:00:56] Agent: And the security code on the back?
[00:00:58] Customer: 341.
[00:01:00] Agent: Perfect. And the billing zip code?
[00:01:02] Customer: 75201.
[00:01:04] Agent: Great, let me process that now. Okay, your payment of $234.87 has been applied successfully. You'll receive a confirmation email shortly and your service will remain active.
[00:01:18] Customer: Oh thank goodness. I was worried about getting cut off.
[00:01:22] Agent: You're all set. Is there anything else I can help you with?
[00:01:25] Customer: No that's it. Thanks Marcus.
[00:01:27] Agent: Thank you for calling Horizon Communications. Have a great day!
[00:01:30] Customer: You too.""",
    },
    "CALL-003": {
        "label": "CALL-003 — Missing recording disclosure",
        "agent_id": "AGENT-031",
        "queue_name": "Technical Support",
        "transcript_text": """[00:00:02] Agent: Horizon Communications technical support, this is David speaking. What seems to be the issue today?
[00:00:08] Customer: Hi, my internet has been going in and out for the past two days. I work from home and this is really impacting my ability to do my job.
[00:00:17] Agent: I understand. Can I get your account number?
[00:00:20] Customer: It's 3345-889-21.
[00:00:24] Agent: Okay I've got your account. Let me run a remote diagnostic on your modem.
[00:00:29] Customer: Sure. Is this going to take long? I have a meeting in 20 minutes.
[00:00:33] Agent: Shouldn't take too long. Running it now.
[00:01:02] Agent: Okay the diagnostic shows some signal instability on your line. There are packet losses happening periodically, which explains the drops you're seeing.
[00:01:12] Customer: So what does that mean for me? Is this something you can fix remotely?
[00:01:17] Agent: I can push a reset to your modem which sometimes clears signal issues. Let me try that.
[00:01:23] Customer: Okay.
[00:01:55] Agent: Alright, I've pushed the reset. Your modem will restart — it takes about two minutes. Can you check after it comes back online and see if things look more stable?
[00:02:05] Customer: Okay, it's restarting now... okay it's back. Let me run a speed test... Yeah the speeds look better actually.
[00:02:22] Agent: Great. The signal instability may have been caused by line noise. If the issue comes back within 48 hours, call us back and we'll escalate to a field technician visit.
[00:02:33] Customer: Okay, and if that happens will there be a charge for the visit?
[00:02:37] Agent: It depends on whether the issue is on our infrastructure or on your side of the demarcation point. I can't say for certain right now.
[00:02:46] Customer: That's a bit vague. I'd like to know before someone comes out.
[00:02:50] Agent: I understand. Just call back if it happens and we'll go over it at that point.
[00:02:56] Customer: Alright. Fine. Thanks.
[00:02:59] Agent: Thank you for calling. Goodbye.""",
    },
    "CALL-004": {
        "label": "CALL-004 — Poor quality (low scores, coaching ticket)",
        "agent_id": "AGENT-055",
        "queue_name": "Customer Retention",
        "transcript_text": """[00:00:05] Agent: This call may be recorded for quality. Horizon Communications, this is Tyler.
[00:00:10] Customer: Hi Tyler, I'm calling because I want to cancel my service. I've been a customer for six years and honestly I'm just fed up.
[00:00:18] Agent: Okay. What's the reason for canceling?
[00:00:21] Customer: The price keeps going up. My bill was $89 when I started and now it's $147. Nobody told me it was going to jump this much.
[00:00:30] Agent: Yeah prices do change. Let me see what's on your account.
[00:00:35] Customer: I mean, I feel like six years of loyalty should count for something. I've never missed a payment.
[00:00:41] Agent: I see that. Okay so looking at your account, you've got the standard internet and cable bundle.
[00:00:48] Customer: Right, and like I said it went up $58 from when I signed up. That's a lot.
[00:00:54] Agent: I can see if there's a promotional rate.
[00:00:57] Customer: I already called last month and someone said they'd look into it and call me back. Nobody ever did.
[00:01:04] Agent: Okay. I don't see a note about that.
[00:01:09] Customer: Well it happened. Can you help me today or not?
[00:01:13] Agent: Let me put you on hold while I check what retention offers are available.
[00:01:17] Customer: Okay.
[00:02:41] Agent: Thanks for holding. So I found a promotional bundle — internet plus cable for $119 per month for 12 months.
[00:02:49] Customer: That's still $30 more than I was paying originally.
[00:02:52] Agent: Right, but it's a savings versus what you're paying now.
[00:02:56] Customer: I guess. Is there anything better than that?
[00:02:59] Agent: That's what I have.
[00:03:03] Customer: What happens after the 12 months?
[00:03:06] Agent: It would go back to the standard rate.
[00:03:09] Customer: So I'd be in the same position again next year.
[00:03:12] Agent: Potentially, yeah.
[00:03:15] Customer: I'm going to think about it. This isn't really the resolution I was hoping for.
[00:03:21] Agent: Okay. Do you want me to note that on the account?
[00:03:24] Customer: I guess. I'm pretty disappointed honestly.
[00:03:28] Agent: Alright. Well let us know what you decide. Is there anything else?
[00:03:33] Customer: No. Bye.
[00:03:35] Agent: Goodbye.""",
    },
    "CALL-005": {
        "label": "CALL-005 — Combined worst case (PCI + poor quality)",
        "agent_id": "AGENT-009",
        "queue_name": "Payment Processing",
        "transcript_text": """[00:00:04] Agent: Horizon Communications, this is Kevin, how can I help you?
[00:00:09] Customer: Hi, I need to pay my bill and I also want to talk about a refund I was promised.
[00:00:15] Agent: Sure. Account number?
[00:00:17] Customer: 9912-443-77.
[00:00:21] Agent: Got it. Balance is $312.50. Go ahead with your payment?
[00:00:26] Customer: Yes, I'll use my card. Number is 4929 0000 0000 1000.
[00:00:34] Agent: Expiration?
[00:00:36] Customer: 11/26.
[00:00:38] Agent: Security code?
[00:00:40] Customer: 782.
[00:00:42] Agent: Zip?
[00:00:43] Customer: 90210.
[00:00:46] Agent: Okay processing. Payment went through. Now about that refund?
[00:00:51] Customer: Yes, I was overcharged two months ago. Someone told me I'd get a credit but it never showed up. I've been calling about this for weeks.
[00:01:01] Agent: Let me look at the account... I see a note here from six weeks ago mentioning an adjustment but I don't see the credit applied.
[00:01:11] Customer: Right, that's the problem. It's $45.
[00:01:14] Agent: I'm going to have to escalate this to our billing adjustments team.
[00:01:18] Customer: I've already been escalated twice. Can't you just apply the credit?
[00:01:23] Agent: I don't have the access level to apply credits over $25.
[00:01:27] Customer: Then transfer me to someone who does.
[00:01:30] Agent: I can transfer you, but the wait time over there is usually pretty long right now.
[00:01:36] Customer: I've been dealing with this for six weeks. I'll wait.
[00:01:40] Agent: Okay I'll transfer you.
[00:01:43] Customer: Wait — before you do, what's the name of the team you're transferring me to? Last time no one knew where I was transferred and I got disconnected.
[00:01:52] Agent: Billing adjustments.
[00:01:54] Customer: And you're giving them context about my issue, right? You're not just cold-transferring me?
[00:01:59] Agent: I'll leave a note.
[00:02:02] Customer: A note? Not a warm transfer?
[00:02:05] Agent: I'm not able to do a warm transfer from this queue.
[00:02:09] Customer: This is really frustrating. Every time I call I have to start over from scratch.
[00:02:14] Agent: I understand. Do you want me to transfer?
[00:02:17] Customer: Fine. Go ahead.
[00:02:19] Agent: Transferring now. Thank you for your patience.
[00:02:23] Customer: I wouldn't call it patience at this point.""",
    },
}

SEVERITY_COLORS = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🟢"
}


def render():
    st.subheader("📞 Contact Center Intelligence Suite")
    st.caption("PCI-DSS compliance scanner + quality scorecard + remediation tickets.")

    try:
        health_check()
        st.success("Agent online", icon="🟢")
    except Exception:
        st.error("Agent offline — check backend URL", icon="🔴")
        return

    st.divider()

    call_id = st.selectbox(
        "Select a call transcript:",
        list(SAMPLE_CALLS.keys()),
        format_func=lambda k: SAMPLE_CALLS[k]["label"]
    )
    call = SAMPLE_CALLS[call_id]

    if st.button("Analyze Call", type="primary", key="agent2_run"):
        with st.spinner("Scanning transcript..."):
            try:
                result = analyze_transcript(
                    call_id=call_id,
                    transcript_text=call["transcript_text"],
                    agent_id=call["agent_id"],
                    queue_name=call["queue_name"]
                )
            except Exception as e:
                st.error(f"Request failed: {e}")
                return

        if result.get("cached"):
            st.caption("⚡ Returned from audit cache — scores are an audit record.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### PCI Compliance")
            pci = result.get("pci_result", {})
            if pci.get("is_fully_compliant"):
                st.success("✅ Fully Compliant")
            else:
                st.error(f"🚨 {pci.get('total_violations', 0)} violation(s) found")
                for v in pci.get("violations", []):
                    icon = SEVERITY_COLORS.get(v["severity"], "⚪")
                    st.markdown(f"{icon} **{v['violation_type']}**")
                    st.caption(f"At ~{v['timestamp_offset_seconds']}s — {v['transcript_excerpt'][:80]}...")
                    st.caption(f"Action: {v['remediation_action']}")
                    st.divider()

        with col2:
            st.markdown("#### Quality Scorecard")
            sc = result.get("scorecard", {})
            if sc:
                overall = sc.get("overall_score", 0)
                color = "🟢" if overall >= 4 else "🟡" if overall >= 3 else "🔴"
                st.metric("Overall Score", f"{color} {overall:.1f} / 5.0")
                st.caption(sc.get("executive_summary", ""))
                st.caption(f"Priority to improve: **{sc.get('coaching_priority', '')}**")
                st.markdown("**Dimension Scores**")
                for dim in sc.get("dimension_scores", []):
                    score = dim.get("score", 0)
                    bar = "█" * score + "░" * (5 - score)
                    st.text(f"{dim['dimension'][:22]:<22} {bar} {score}/5")

        with col3:
            st.markdown("#### Remediation Ticket")
            ticket = result.get("ticket")
            if ticket:
                sev = ticket.get("severity_level", "")
                icon = SEVERITY_COLORS.get(sev, "⚪")
                st.markdown(f"**{icon} {sev} — {ticket.get('trigger_reason', '')}**")
                st.markdown(f"**Issue:** {ticket.get('primary_issue', '')}")
                st.markdown("**Coaching Script:**")
                st.info(ticket.get("supervisor_coaching_script", ""))
                st.markdown("**Required Actions:**")
                for action in ticket.get("required_actions", []):
                    st.markdown(f"- {action}")
            else:
                st.success("✅ No ticket required")
                st.caption("Call met compliance and quality thresholds.")
