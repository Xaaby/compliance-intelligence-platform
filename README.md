# 🛡️ Compliance Intelligence Platform

A unified Streamlit dashboard that surfaces three production AI agents — infrastructure compliance, contact center QA, and government citizen intelligence — through a single tabbed interface. No business logic lives here; this app is a pure presentation layer that calls three live FastAPI backends on GCP Cloud Run.

---

## Architecture

```
Browser
  └── compliance-intelligence-platform (Cloud Run · port 8080 · Streamlit)
        │
        ├── Tab 1: 🔧 DevOps Compliance
        │     └── POST /chat, GET /health
        │           └── gcp-devops-backend (Cloud Run · FastAPI)
        │                 └── SOC 2 / NIST pipeline monitoring · Gemini
        │
        ├── Tab 2: 📞 Contact Center QA
        │     └── POST /analyze, GET /health
        │           └── ccai-quality-agent-api (Cloud Run · FastAPI)
        │                 └── PCI-DSS scan · quality scorecard · remediation tickets · Gemini
        │
        └── Tab 3: 🏛️ Government Intelligence
              └── POST /classify, POST /query-cjis, GET /health
                    └── ccai-gov-intelligence-api (Cloud Run · FastAPI)
                          └── 311 classifier · CJIS RAG · Gemini
```

---

## Live URLs

| Service | URL |
|---|---|
| **Compliance Intelligence Platform** | https://compliance-intelligence-platform-786562162192.us-central1.run.app |
| GCP DevOps Compliance Agent (backend) | https://gcp-devops-backend-786562162192.us-central1.run.app |
| Contact Center Intelligence Suite (API) | https://ccai-quality-agent-api-786562162192.us-central1.run.app |
| Government Citizen Intelligence Platform (API) | https://ccai-gov-intelligence-api-786562162192.us-central1.run.app |

---

## Demo Order

1. **Tab 1 — DevOps Compliance:** Type *"Give me a full audit report for the last 7 days"* → show SOC 2 compliance result with tools called
2. **Tab 2 — Contact Center QA:** Select `CALL-002` → show PCI violation with timestamp and remediation ticket
3. **Tab 2:** Select `CALL-001` → show fully compliant result → *"No false positives"*
4. **Tab 3 — Government Intelligence (311 mode):** Select `REQ-005` → show 5-department work order decomposition
5. **Tab 3 (CJIS mode):** Select `Q-001` → show cited policy answer with section reference
6. **Tab 3 (CJIS mode):** Type an out-of-scope question → show `cannot_answer` state
7. Close: *"Three verticals. One architecture. GCP-native, Gemini-powered, fully deployed."*

---

## GCP Services Used

- **Cloud Run** — hosts this platform app and all three agent backends
- **Artifact Registry** — Docker image storage (`compliance-platform` repo)
- **Workload Identity Federation** — keyless GitHub Actions authentication
- **Cloud Logging** — runtime logs via `logging.logWriter` role
- **Vertex AI / Gemini** — handled entirely within the three agent backends; this app has no Gemini SDK

---

## Running Locally

```bash
# 1. Clone the repo
git clone https://github.com/Xaaby/compliance-intelligence-platform
cd compliance-intelligence-platform

# 2. Create .env from example (URLs already point to live backends)
cp .env.example .env

# 3a. Run with Docker Compose
docker compose up --build

# 3b. Or run directly (requires Python 3.11+)
pip install -r app/requirements.txt
streamlit run app/streamlit_app.py --server.port 8080

# Open http://localhost:8080
```

The platform calls the live Cloud Run backends even during local development — no local agent logic required.

---

## GitHub Actions Secrets Required



| Secret | Value |
|---|---|
| `WIF_PROVIDER` |
| `WIF_SERVICE_ACCOUNT` | 
| `GCP_PROJECT_ID` |
| `AGENT1_URL` | `https://gcp-devops-backend-786562162192.us-central1.run.app` |
| `AGENT2_URL` | `https://ccai-quality-agent-api-786562162192.us-central1.run.app` |
| `AGENT3_URL` | `https://ccai-gov-intelligence-api-786562162192.us-central1.run.app` |

> **WIF scope:** Verify the Workload Identity Pool attribute condition covers
---

## Repo Structure

```
compliance-intelligence-platform/
├── app/
│   ├── streamlit_app.py          ← entry point
│   ├── config.py                 ← env vars, backend URLs, timeouts
│   ├── requirements.txt
│   ├── api_clients/
│   │   ├── agent1_client.py      ← httpx client for DevOps agent
│   │   ├── agent2_client.py      ← httpx client for CCAI agent
│   │   └── agent3_client.py      ← httpx client for Gov agent
│   └── tabs/
│       ├── tab_devops.py         ← Tab 1 UI
│       ├── tab_ccai.py           ← Tab 2 UI
│       └── tab_gov.py            ← Tab 3 UI
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .github/workflows/deploy.yml  ← CI/CD to Cloud Run
```
