import os

AGENT1_URL = os.environ.get("AGENT1_URL", "https://gcp-devops-backend-786562162192.us-central1.run.app")
AGENT2_URL = os.environ.get("AGENT2_URL", "https://ccai-quality-agent-api-786562162192.us-central1.run.app")
AGENT3_URL = os.environ.get("AGENT3_URL", "https://ccai-gov-intelligence-api-786562162192.us-central1.run.app")

HTTP_TIMEOUT = 120

AGENT1_NAME = "DevOps Compliance Agent"
AGENT2_NAME = "Contact Center Intelligence Suite"
AGENT3_NAME = "Government Citizen Intelligence Platform"
