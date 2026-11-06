"""Run every test prompt against the latest version of the agent and save the results.

    python src/tests/run_batch_tests.py <experiment-name>       (run from the genaiops folder)
    e.g.  python src/tests/run_batch_tests.py baseline

Creates, in experiments/<experiment-name>/:
  agent-responses.json   the prompts, full responses and token usage
  evaluation.csv         a scoring sheet: fill in the 1-5 scores yourself (only created if it doesn't exist)
"""
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab_common import ROOT, explain_error, get_project_client, load_settings, with_retries  # noqa: E402

SCORE_COLUMNS = ["intent_resolution", "relevance", "groundedness"]


def load_test_prompts(folder):
    return {p.stem: p.read_text(encoding="utf-8").strip() for p in sorted(Path(folder).glob("*.txt"))}


def ask_agent(openai_client, agent_name, prompt_text):
    conversation = openai_client.conversations.create()
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": prompt_text}],
    )
    return openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
        input="",
    )


def write_scoring_sheet(path, results):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(["test_prompt", "agent_response_excerpt", *SCORE_COLUMNS, "total_tokens", "comments"])
        for r in results:
            excerpt = " ".join(r["response"].split())[:90] + "..."
            w.writerow([r["test_name"], excerpt, "", "", "", r["token_usage"]["total_tokens"] or "", ""])


def run_batch_tests(experiment_name):
    endpoint, agent_name = load_settings()
    prompts = load_test_prompts(Path(__file__).parent / "test-prompts")
    if not prompts:
        sys.exit("No test prompts found in src/tests/test-prompts/")

    print(f"Running {len(prompts)} test prompts for experiment: {experiment_name}")
    print("=" * 70)
    client = get_project_client(endpoint)
    try:
        agent = client.agents.get(agent_name)
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"ERROR: agent '{agent_name}' not found or not reachable.\n  {exc}\n"
                 f"Create it first:  python src/agents/trail_guide_agent/trail_guide_agent.py\n"
                 f"What to do: {explain_error(exc)}")
    latest = agent.versions.latest if hasattr(agent, "versions") and hasattr(agent.versions, "latest") else None
    version = getattr(latest, "version", "?")
    model = getattr(getattr(latest, "definition", None), "model", "?")
    print(f"Using agent: {agent.name} (version: {version}, model: {model})")

    openai_client = client.get_openai_client()
    results = []
    for name, text in prompts.items():
        print(f"\nTesting: {name}\n   Prompt: {text[:60]}...")
        try:
            response = with_retries(lambda: ask_agent(openai_client, agent_name, text))
        except Exception as exc:  # noqa: BLE001
            sys.exit(f"ERROR while testing '{name}': {exc}\nWhat to do: {explain_error(exc)}")
        reply = getattr(response, "output_text", None) or str(response)
        usage = getattr(response, "usage", None)
        tokens = {
            "prompt_tokens": getattr(usage, "input_tokens", None),
            "completion_tokens": getattr(usage, "output_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }
        results.append({"test_name": name, "prompt": text, "response": reply,
                        "token_usage": tokens, "response_id": getattr(response, "id", None)})
        print(f"   Response captured ({tokens['total_tokens']} tokens)")

    out_dir = ROOT / "experiments" / experiment_name
    out_dir.mkdir(parents=True, exist_ok=True)
    data = {"experiment": experiment_name, "timestamp": datetime.now().isoformat(timespec="seconds"),
            "agent_name": agent_name, "agent_version": version, "model": model, "test_results": results}
    (out_dir / "agent-responses.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    sheet = out_dir / "evaluation.csv"
    if not sheet.exists():
        write_scoring_sheet(sheet, results)
        sheet_msg = f"Scoring sheet created: {sheet.relative_to(ROOT)} (fill in the 1-5 scores)"
    else:
        sheet_msg = f"Scoring sheet already exists, not overwritten: {sheet.relative_to(ROOT)}"

    total = sum(r["token_usage"]["total_tokens"] or 0 for r in results)
    print("\n" + "=" * 70)
    print(f"Results saved to: {(out_dir / 'agent-responses.json').relative_to(ROOT)}")
    print(sheet_msg)
    print(f"Total tests: {len(results)}")
    print(f"Total tokens used: {total}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python src/tests/run_batch_tests.py <experiment-name>\n"
                 "Example: python src/tests/run_batch_tests.py baseline")
    run_batch_tests(sys.argv[1])
