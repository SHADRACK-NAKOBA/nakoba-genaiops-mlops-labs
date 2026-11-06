"""Create the .env file from your azd environment (Nakoba GenAIOps labs).

    python scripts/make_env.py

Why a script instead of `azd env get-values > .env`?
In Windows PowerShell, `>` saves the file as UTF-16, which Python can't read, so every
later script fails with a confusing KeyError. This script always writes UTF-8 and also
adds AGENT_NAME and MODEL_NAME for you.
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # the genaiops folder
ENV_FILE = ROOT / ".env"
DEFAULTS = {"AGENT_NAME": "trail-guide", "MODEL_NAME": "gpt-5.1"}


def main() -> None:
    azd = shutil.which("azd")
    if not azd:
        sys.exit("ERROR: 'azd' was not found. Install the Azure Developer CLI (docs/00-prerequisites.md), "
                 "then close and reopen VS Code.")
    try:
        out = subprocess.run([azd, "env", "get-values"], cwd=ROOT, capture_output=True,
                             text=True, encoding="utf-8", check=True).stdout
    except subprocess.CalledProcessError as exc:
        sys.exit("ERROR: 'azd env get-values' failed. Run 'azd up' first, from the genaiops folder.\n"
                 + (exc.stderr or exc.stdout or ""))

    values = {}
    for line in out.splitlines():
        line = line.strip().lstrip("﻿")
        if "=" in line and not line.startswith("#"):
            key, _, val = line.partition("=")
            values[key.strip()] = val.strip().strip('"')

    if not values.get("AZURE_AI_PROJECT_ENDPOINT"):
        sys.exit("ERROR: AZURE_AI_PROJECT_ENDPOINT is missing. Did 'azd up' finish successfully?")

    # keep any AGENT_NAME / MODEL_NAME the student already changed
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            key, _, val = line.partition("=")
            if key.strip() in DEFAULTS and val.strip():
                values[key.strip()] = val.strip().strip('"')
    for key, val in DEFAULTS.items():
        values.setdefault(key, val)

    ENV_FILE.write_text("".join(f'{k}="{v}"\n' for k, v in values.items()), encoding="utf-8")
    print(f"Wrote {ENV_FILE} ({len(values)} values, UTF-8)")
    print(f"  AZURE_AI_PROJECT_ENDPOINT = {values['AZURE_AI_PROJECT_ENDPOINT']}")
    print(f"  AGENT_NAME = {values['AGENT_NAME']}   MODEL_NAME = {values['MODEL_NAME']}")
    if "AZURE_OPENAI_DEPLOYMENT_NAMES" in values:
        print(f"  Deployed models: {values['AZURE_OPENAI_DEPLOYMENT_NAMES']}")


if __name__ == "__main__":
    main()
