"""Compare all experiments side by side: average scores and token usage.

    python src/tests/compare_experiments.py        (run from the genaiops folder)

Reads experiments/*/agent-responses.json and experiments/*/evaluation.csv.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCORES = ["intent_resolution", "relevance", "groundedness"]


def load(exp_dir):
    data = json.loads((exp_dir / "agent-responses.json").read_text(encoding="utf-8"))
    tokens = sum(r["token_usage"].get("total_tokens") or 0 for r in data["test_results"])
    out_tokens = sum(r["token_usage"].get("completion_tokens") or 0 for r in data["test_results"])
    avg, missing = {}, False
    sheet = exp_dir / "evaluation.csv"
    if sheet.exists():
        with open(sheet, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        for col in SCORES:
            vals = []
            for row in rows:
                key = next((k for k in row if k and k.strip().lower() == col), None)
                try:
                    vals.append(float(row[key]))
                except (TypeError, ValueError, KeyError):
                    missing = True
            avg[col] = sum(vals) / len(vals) if vals else None
    else:
        missing = True
    return {"name": exp_dir.name, "model": data.get("model", "?"), "tokens": tokens,
            "out_tokens": out_tokens, "avg": avg, "missing": missing}


def main():
    exps = [load(d) for d in sorted((ROOT / "experiments").glob("*")) if (d / "agent-responses.json").exists()]
    if not exps:
        print("No experiments yet. Run: python src/tests/run_batch_tests.py baseline")
        return
    base = next((e for e in exps if e["name"] == "baseline"), None)
    header = f"{'experiment':<20}{'model':<12}{'intent':>8}{'relev.':>8}{'ground.':>8}{'avg':>7}{'tokens':>9}{'vs base':>9}"
    print(header)
    print("-" * len(header))
    for e in exps:
        vals = [e["avg"].get(c) for c in SCORES]
        cells = "".join(f"{v:>8.2f}" if v is not None else f"{'-':>8}" for v in vals)
        known = [v for v in vals if v is not None]
        overall = f"{sum(known) / len(known):>7.2f}" if known else f"{'-':>7}"
        change = ""
        if base and base["tokens"] and e is not base:
            change = f"{(e['tokens'] - base['tokens']) / base['tokens'] * 100:+.0f}%"
        print(f"{e['name']:<20}{str(e['model'])[:11]:<12}{cells}{overall}{e['tokens']:>9}{change:>9}")
    if any(e["missing"] for e in exps):
        print("\n'-' = scores not filled in yet in that experiment's evaluation.csv")
    print("\nDecide: the cheapest option (fewest tokens / smaller model) whose scores stay close to the baseline.")


if __name__ == "__main__":
    main()
