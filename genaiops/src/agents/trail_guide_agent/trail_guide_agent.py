"""Create a new version of the Trail Guide Agent in Microsoft Foundry.

    python src/agents/trail_guide_agent/trail_guide_agent.py      (run from the genaiops folder)

Each run creates a NEW VERSION of the agent named AGENT_NAME (default: trail-guide).
To change the agent's behaviour, change the PROMPT FILE line below (v1 -> v2 -> v3 -> v4)
or the MODEL line, save, and run the script again.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # so 'lab_common' can be imported
from lab_common import explain_error, get_project_client, load_settings  # noqa: E402

from azure.ai.projects.models import PromptAgentDefinition  # noqa: E402

endpoint, agent_name = load_settings()

# Read instructions from prompt file
prompt_file = Path(__file__).parent / 'prompts' / 'v1_instructions.txt'
with open(prompt_file, 'r', encoding='utf-8') as f:
    instructions = f.read().strip()

project_client = get_project_client(endpoint)

try:
    agent = project_client.agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(
            model=os.getenv("MODEL_NAME", "gpt-5.1"),
            instructions=instructions,
        ),
        description=f"Prompt: {prompt_file.name}",
    )
except Exception as exc:  # noqa: BLE001
    print(f"ERROR: could not create the agent.\n  {exc}\n\nWhat to do: {explain_error(exc)}")
    sys.exit(1)

print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")
print(f"  prompt: {prompt_file.name}   model: {getattr(agent.definition, 'model', '?')}")
