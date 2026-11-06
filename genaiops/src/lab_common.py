"""Shared helpers for the Nakoba GenAIOps lab scripts."""
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent        # the genaiops folder


def load_settings():
    """Load genaiops/.env no matter which folder you run the script from."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        sys.exit(f"ERROR: {env_file} not found. From the genaiops folder run:  python scripts/make_env.py")
    load_dotenv(env_file, override=True, encoding="utf-8")
    if not os.getenv("AZURE_AI_PROJECT_ENDPOINT"):
        sys.exit("ERROR: AZURE_AI_PROJECT_ENDPOINT is empty in .env. Run:  python scripts/make_env.py")
    return os.environ["AZURE_AI_PROJECT_ENDPOINT"], os.getenv("AGENT_NAME", "trail-guide")


def get_project_client(endpoint):
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential
    return AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())


def explain_error(exc):
    """Turn the most common Azure errors into a clear next step."""
    text = str(exc)
    hints = [
        (("DefaultAzureCredential failed", "az login", "CredentialUnavailable"),
         "You're not signed in. Run:  az login   (then run this script again)"),
        (("PermissionDenied", "AuthorizationFailed", "does not have permission", "401", "403"),
         "Permission problem. Role assignments from 'azd up' can take up to 10 minutes to "
         "work: wait, then run again. Also check 'az account show' is the subscription you deployed to."),
        (("DeploymentNotFound", "deployment not found", "model_not_found", "does not exist"),
         "The model deployment wasn't found. MODEL_NAME (in .env or the script) must be exactly "
         "'gpt-5.1' or 'gpt-5-mini' - the deployments created by 'azd up'."),
        (("429", "RateLimit", "rate limit", "Too Many Requests"),
         "Rate limit reached. Wait a minute and run again."),
        (("getaddrinfo", "Name or service not known", "ConnectError"),
         "Can't reach the endpoint. Check your internet connection and AZURE_AI_PROJECT_ENDPOINT in .env."),
    ]
    for needles, hint in hints:
        if any(n.lower() in text.lower() for n in needles):
            return hint
    return "See docs/06-troubleshooting.md for this error."


def with_retries(fn, attempts=4, wait=20):
    """Retry on rate limits (HTTP 429), which small model quotas hit often."""
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            if i < attempts - 1 and ("429" in msg or "rate limit" in msg.lower() or "Too Many" in msg):
                print(f"   rate limited - waiting {wait}s and retrying ({i + 1}/{attempts - 1})...")
                time.sleep(wait)
                continue
            raise
