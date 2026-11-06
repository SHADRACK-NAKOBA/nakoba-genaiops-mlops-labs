# Track 1 – GenAIOps with Microsoft Foundry

Build, version, optimize and fine-tune-plan an AI agent: the **Adventure Works Trail Guide Agent** (a fictional outdoor company) on **Microsoft Foundry**, using Python, Git and the Azure Developer CLI.

| # | Lab | You learn | Time | Cost |
|---|---|---|---|---|
| 0 | [Prerequisites](docs/00-prerequisites.md) | Install VS Code, Python, Git, Azure CLI, azd | 30–45 min | Free |
| 1 | [Set up Microsoft Foundry](docs/01-setup-foundry.md) | Your own repo, `azd up`, `.env`, virtual environment | 20 min | Cents |
| 2 | [Develop prompt and agent versions](docs/02-prompt-and-agent-versions.md) | Prompt engineering, agent versions v1→v3, Git tags | 30 min | Cents |
| 3 | [Design and optimize prompts](docs/03-design-optimize-prompts.md) | Baseline, experiment branches, batch tests, scoring, model comparison, merge | 45 min | Cents |
| 4 | [Optimize agents with fine-tuning](docs/04-fine-tuning.md) | SFT vs DPO vs RFT, choosing valid training data | 20 min | Free |
| – | [Share and clean up](docs/05-share-and-cleanup.md) | LinkedIn post, `azd down --purge` | 10 min | – |
| – | [Troubleshooting](docs/06-troubleshooting.md) | Fixes for every common error | – | – |
| – | [Interview questions](docs/07-interview-questions.md) | Explain the work in an interview | – | – |

Do them in order: Labs 2 and 3 use the resources from Lab 1. Lab 4 needs only a browser.

```
genaiops/
├── azure.yaml  infra/                   ← azd + Bicep: Foundry project, gpt-5.1, gpt-5-mini, monitoring
├── requirements.txt  .env.example
├── scripts/make_env.py                  ← writes .env (UTF-8) from your azd environment
├── src/
│   ├── lab_common.py                    ← loads .env, connects, explains common errors
│   ├── agents/trail_guide_agent/
│   │   ├── trail_guide_agent.py         ← creates a new agent version
│   │   └── prompts/ v1, v2, v3, v4_optimized_concise
│   └── tests/
│       ├── test-prompts/                ← 5 fixed test questions
│       ├── run_batch_tests.py           ← runs them, saves responses + a scoring sheet
│       └── compare_experiments.py       ← compares scores and tokens across experiments
├── experiments/                         ← your results (created in Lab 3)
├── finetuning-lab/                      ← interactive SFT/DPO/RFT lab (open index.html)
└── docs/                                ← this guide
```

## Fixed compared with the original exercises

| Problem students hit | Fix |
|---|---|
| Labs used **gpt-4.1 / gpt-4.1-mini**, which are deprecated, so **new subscriptions can't deploy them**. The template deployed only gpt-5-mini while the script defaulted to gpt-5.1 | The template now deploys **gpt-5.1** and **gpt-5-mini**, matching the scripts and the guide |
| `azd env get-values > .env` saves **UTF-16** in Windows PowerShell, so scripts fail with `KeyError` | `python scripts/make_env.py` writes UTF-8 and adds `AGENT_NAME` and `MODEL_NAME` |
| `Activate.ps1` blocked: *running scripts is disabled* | Guide includes the `Set-ExecutionPolicy -Scope Process` line |
| Advice to use `az login --username --password` (fails with required MFA) | `--use-device-code` instead |
| `azd up` asked for an extension and an extra parameter, and built an unused container registry | Template simplified: no extension, default principal type, no registry |
| SDK pinned to a pre-release (`2.0.0b4`) | Pinned to GA **azure-ai-projects 2.10.0**; requirements trimmed to 4 packages |
| Scripts worked only from one folder | Scripts find `.env` from any folder and give clear fixes for common Azure errors |
| Copy-paste errors in the guide: unclosed quote in `git commit`, smart quotes in `git merge`/`git tag`, CSV comments with commas | Corrected commands; the batch script creates the scoring sheet for you |
| Baseline results weren't committed, so branches couldn't compare against them | Baseline is committed on main before branching; `compare_experiments.py` compares all three |
| Made-up "42% fewer tokens" result | Students measure and decide from **their own** numbers |
| Fine-tuning lab: "download the JSONL" (it's shown on the page, not downloaded) | Guide describes what really happens; the lab runs locally from this repo |
| `azd down` left a soft-deleted resource that blocks re-deploying | `azd down --purge` |

*Based on Microsoft Learn's open-source GenAIOps exercises ([MicrosoftLearning/mslearn-genaiops](https://github.com/MicrosoftLearning/mslearn-genaiops), MIT licence). Adventure Works is a fictional company.*
