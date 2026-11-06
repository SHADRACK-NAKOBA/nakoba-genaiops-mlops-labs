# GenAIOps Lab 3 – Design and optimize prompts

[⬅ Prompt and agent versions](02-prompt-and-agent-versions.md) | [🏠 Track home](../README.md) | [Next: Fine-tuning ➡](04-fine-tuning.md)

**Scenario.** The Trail Guide Agent runs the **v3** production prompt on **gpt-5.1**. Before changing anything you **measure a baseline**. Then you run two experiments, each on its own **Git branch**:

1. **Token reduction:** a concise **v4** prompt on the same model.
2. **Model comparison:** the v4 prompt on the cheaper **gpt-5-mini**.

You score every answer, compare quality against tokens (cost), and **merge the winner** into `main`.

**Time:** about 45 minutes. **Cost:** a few cents.

| Concept | In this lab |
|---|---|
| **Baseline** | Scores and tokens for v3 + gpt-5.1, the reference point every experiment is compared with |
| **Prompt versioning** | `v3_instructions.txt` (production) vs `v4_optimized_concise.txt` (experiment) |
| **Batch testing** | `run_batch_tests.py` sends the same 5 test prompts every time and records tokens |
| **Experiment branches** | `experiment/optimized-concise`, `experiment/gpt5mini`: changes stay off `main` until proven |
| **Production decision** | Pick the cheapest option whose quality stays close to the baseline |

> Before you start: [setup](01-setup-foundry.md) done (Lab 2 is recommended but not required). Terminal in **genaiops** with **(.venv)** active.

```
genaiops/
├── experiments/                      ← created by the batch script
│   ├── baseline/            agent-responses.json + evaluation.csv
│   ├── optimized-concise/   agent-responses.json + evaluation.csv
│   └── gpt5mini/            agent-responses.json + evaluation.csv
└── src/
    ├── agents/trail_guide_agent/
    │   ├── trail_guide_agent.py      ← you change the prompt / model line per experiment
    │   └── prompts/ v1 … v3_instructions.txt, v4_optimized_concise.txt
    └── tests/
        ├── test-prompts/             ← 5 realistic questions
        ├── run_batch_tests.py        ← runs them and saves the results + a scoring sheet
        └── compare_experiments.py    ← side-by-side comparison
```

**Workflow for every experiment:** branch → change one thing → deploy the agent → batch test → score → commit.

---

## 3.1 Establish the baseline (on main)

1. Make sure you're on **main**:
   ```bash
   git checkout main
   ```
2. Open **src/agents/trail_guide_agent/trail_guide_agent.py** and check these two lines (fix and save if needed):
   ```python
   prompt_file = Path(__file__).parent / 'prompts' / 'v3_instructions.txt'
   ```
   ```python
   model=os.getenv("MODEL_NAME", "gpt-5.1"),
   ```
   If you changed the file, commit it:
   ```bash
   git add src/agents/trail_guide_agent/trail_guide_agent.py
   git commit -m "Set baseline agent configuration to v3 prompt"
   ```
   (*nothing to commit*? It was already right. Continue.)
3. Deploy the baseline agent version:
   ```bash
   python src/agents/trail_guide_agent/trail_guide_agent.py
   ```
4. Run the 5 test prompts:
   ```bash
   python src/tests/run_batch_tests.py baseline
   ```
   Expected (token numbers will differ):
   ```
   Running 5 test prompts for experiment: baseline
   Using agent: trail-guide (version: 4, model: gpt-5.1)
   Testing: day-hike-gear ... Response captured (812 tokens)
   ...
   Results saved to: experiments/baseline/agent-responses.json
   Scoring sheet created: experiments/baseline/evaluation.csv (fill in the 1-5 scores)
   Total tokens used: 4210
   ```
5. Read the answers: open **experiments/baseline/agent-responses.json** in VS Code (each `"response"` is one answer).

### Score the baseline

Open **experiments/baseline/evaluation.csv**. For each row, type a score from **1 to 5** in the three empty score columns, and a short comment:

| Column | Question to ask yourself |
|---|---|
| `intent_resolution` | Did it answer what the user actually asked? |
| `relevance` | Is it on-topic and appropriate for the person asking? |
| `groundedness` | Are the facts accurate and safe (nothing made up)? |

Example of a scored row:
```csv
day-hike-gear,"For a summer day hike in moderate terrain, essential gear includes...",5,5,4,812,"Clear and comprehensive gear list"
```

> ⚠️ Put **"quotes"** around a comment that contains a comma, or the CSV columns shift. Save with **Ctrl+S**.

6. Commit the baseline **on main**, so both experiment branches include it:
   ```bash
   git add experiments/baseline/
   git commit -m "Baseline: v3 prompt on gpt-5.1"
   ```

## 3.2 Experiment 1 – Token reduction (v4 prompt)

1. Create the experiment branch:
   ```bash
   git checkout -b experiment/optimized-concise
   ```
2. Look at the test prompts (they're the same for every experiment):
   ```bash
   ls src/tests/test-prompts/
   cat src/tests/test-prompts/day-hike-gear.txt
   ```
   You'll see 5 files: `day-hike-gear`, `overnight-camping`, `three-day-backpacking`, `trail-difficulty`, `winter-hiking`.
3. In **trail_guide_agent.py** change the prompt line to v4 and save:
   ```python
   prompt_file = Path(__file__).parent / 'prompts' / 'v4_optimized_concise.txt'
   ```
4. Commit the change on the branch:
   ```bash
   git add src/agents/trail_guide_agent/trail_guide_agent.py
   git commit -m "Configure agent to use v4 optimized-concise prompt"
   ```
5. Deploy and test:
   ```bash
   python src/agents/trail_guide_agent/trail_guide_agent.py
   python src/tests/run_batch_tests.py optimized-concise
   ```
6. Score **experiments/optimized-concise/evaluation.csv** exactly as you did the baseline. Be honest: shorter isn't better if it drops important safety advice.
7. Commit and tag:
   ```bash
   git add experiments/optimized-concise/
   git commit -m "Complete optimized-concise experiment with evaluation"
   git tag experiment-1-optimized-concise
   ```

## 3.3 Experiment 2 – Model comparison (gpt-5-mini)

**Question:** can the smaller, cheaper **gpt-5-mini** keep acceptable quality with the v4 prompt?

1. Branch from experiment 1 (so v4 is already set):
   ```bash
   git checkout -b experiment/gpt5mini
   ```
2. In **trail_guide_agent.py** change the model line and save:
   ```python
   # from:
   model=os.getenv("MODEL_NAME", "gpt-5.1"),
   # to:
   model="gpt-5-mini",
   ```
   Check the prompt line still says `v4_optimized_concise.txt`.
3. Commit, deploy, test:
   ```bash
   git add src/agents/trail_guide_agent/trail_guide_agent.py
   git commit -m "Configure agent to use gpt-5-mini with v4 prompt"
   python src/agents/trail_guide_agent/trail_guide_agent.py
   python src/tests/run_batch_tests.py gpt5mini
   ```
   The agent output now shows `model: gpt-5-mini`.
4. Score **experiments/gpt5mini/evaluation.csv**. Optionally add a `depth` column (1–5): small models are often correct but less detailed.
5. Commit and tag:
   ```bash
   git add experiments/gpt5mini/
   git commit -m "Complete gpt-5-mini experiment with evaluation"
   git tag experiment-2-gpt5mini
   ```

## 3.4 Compare and decide

1. List your experiment branches:
   ```bash
   git branch --list "experiment/*"
   ```
2. This branch (`experiment/gpt5mini`) contains all three result folders. Compare them:
   ```bash
   python src/tests/compare_experiments.py
   ```
   Example output (your numbers will differ):
   ```
   experiment          model         intent  relev. ground.    avg   tokens  vs base
   ---------------------------------------------------------------------------------
   baseline            gpt-5.1         4.60    4.60    4.60   4.60     4210
   gpt5mini            gpt-5-mini      4.00    4.00    4.00   4.00     2380      -43%
   optimized-concise   gpt-5.1         4.80    4.80    4.60   4.73     2450      -42%
   ```
3. Decide with the data:
   - Which option keeps scores **close to the baseline** (within ~0.3)?
   - Which uses the **fewest tokens**? (Tokens ≈ cost; gpt-5-mini also costs much less **per token**.)
   - Which test prompts got worse? Safety questions (`three-day-backpacking`, `winter-hiking`) matter most.

   A typical result: **optimized-concise wins**, with the same or better quality and far fewer tokens. gpt-5-mini is a good option for simple, high-volume questions if cost is critical. **Your scores decide**, not the example.

## 3.5 Merge the winner into main

Below, the winner is `experiment/optimized-concise`. If **gpt5mini** won, use `experiment/gpt5mini` instead.

1. Switch to main and merge:
   ```bash
   git checkout main
   git merge experiment/optimized-concise -m "Merge optimized-concise prompt experiment"
   ```
2. Open **trail_guide_agent.py** on main and check the prompt line now says `v4_optimized_concise.txt`.
   > A merge conflict? VS Code shows the file with *Accept Current / Accept Incoming*. Choose the v4 line, save, then `git add src/agents/trail_guide_agent/trail_guide_agent.py` and `git commit -m "Resolve merge: use v4 prompt"`.
3. Deploy the production version from main:
   ```bash
   python src/agents/trail_guide_agent/trail_guide_agent.py
   ```
4. Tag the release (write the token saving **you** measured):
   ```bash
   git tag -a v4-optimized-prompt -m "Release v4: token-optimized prompt, quality kept vs baseline (see experiments/)"
   ```
5. Push everything to GitHub:
   ```bash
   git push origin main
   git push origin experiment/optimized-concise experiment/gpt5mini
   git push origin --tags
   ```
   On GitHub, your repo now shows the branches, the tags, and the evidence (the `experiments/` folders).

## ✅ Check

- [ ] Three scored experiments: `baseline`, `optimized-concise`, `gpt5mini`
- [ ] `compare_experiments.py` shows scores and token changes
- [ ] The winning branch is merged into main and tagged `v4-optimized-prompt`
- [ ] You can explain your decision with numbers

[⬅ Prompt and agent versions](02-prompt-and-agent-versions.md) | [🏠 Track home](../README.md) | [Next: Fine-tuning ➡](04-fine-tuning.md)
