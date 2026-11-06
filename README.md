# Nakoba Hands-on Labs: GenAIOps with Microsoft Foundry & MLOps with Azure Machine Learning

Seven hands-on labs in two tracks. Every page is click by click, every script was tested, and the known blockers from the original exercises are fixed.

## 🧭 Track 1 – GenAIOps with Microsoft Foundry → [`genaiops/`](genaiops/README.md)

Build and improve the **Trail Guide Agent** (a fictional Adventure Works product) on Microsoft Foundry, with Python, Git and the Azure Developer CLI.

| # | Lab | What you do |
|---|---|---|
| 0 | [Prerequisites for GenAIOps labs](genaiops/docs/00-prerequisites.md) | Install VS Code, Python, Git, Azure CLI, azd |
| 1 | [Set up Microsoft Foundry](genaiops/docs/01-setup-foundry.md) | Your own repo, `azd up` (gpt-5.1 + gpt-5-mini), `.env`, venv |
| 2 | [Develop prompt and agent versions](genaiops/docs/02-prompt-and-agent-versions.md) | Prompt v1→v3, agent versions, Git tags, compare in the portal |
| 3 | [Design and optimize prompts](genaiops/docs/03-design-optimize-prompts.md) | Baseline, experiment branches, batch tests, scoring, model comparison, merge the winner |
| 4 | [Optimize AI agents with fine-tuning](genaiops/docs/04-fine-tuning.md) | Choose SFT / DPO / RFT and the valid training data (interactive, free) |

## 🔁 Track 2 – MLOps with Azure Machine Learning → [`mlops/`](mlops/README.md)

| # | Lab | What you do |
|---|---|---|
| 0 | [Provision the workspace](mlops/docs/01-provision-workspace.md) | One script: workspace, compute, data |
| 1 | [Run pipelines in Azure ML](mlops/docs/02-run-pipelines.md) | Components → a 2-step training pipeline |
| 2 | [Create and explore the Responsible AI dashboard](mlops/docs/03-responsible-ai-dashboard.md) | Error analysis, feature importance, cohorts |
| 3 | [Automate model training with GitHub Actions](mlops/docs/04-github-actions.md) | Service principal, secrets, workflow, PR-triggered training, branch protection |

The tracks are independent: start with either. Labs inside a track build on each other, so do them in order.

## 🚀 Get started

| Track | First step |
|---|---|
| GenAIOps | Click **Use this template → Create a new repository** (or **Fork**) at the top of this page, then follow [Prerequisites](genaiops/docs/00-prerequisites.md) → [Setup](genaiops/docs/01-setup-foundry.md). You need **your own copy** because you'll commit, tag, branch and push. |
| MLOps | Labs 1–2 run in the browser (Azure Cloud Shell + ML studio): start at [Provision the workspace](mlops/docs/01-provision-workspace.md). Lab 3 uses your own copy of this repo. |

**You need:** an Azure subscription (Free Trial works; **Owner** for the GenAIOps track) and a GitHub account. **Cost:** a few cents to a few dollars in total, if you follow the clean-up steps at the end of each track.

## Repository layout

```
nakoba-genaiops-mlops-labs/
├── genaiops/            ← Track 1: azd + Bicep infra, agent scripts, prompts, tests, fine-tuning lab, docs
├── mlops/               ← Track 2: setup scripts, data, model, notebooks, training job, docs
└── .github/workflows/   ← the GitHub Actions workflow for MLOps Lab 3
```

## Interview prep

Each track ends with interview questions and a 60-second pitch: [GenAIOps](genaiops/docs/07-interview-questions.md) · [MLOps](mlops/docs/07-interview-questions.md).

## Need help?

Every track has a troubleshooting page: [GenAIOps](genaiops/docs/06-troubleshooting.md) · [MLOps](mlops/docs/06-troubleshooting.md). Still stuck? Post the lab and step number with a screenshot of the full error (hide secrets and subscription IDs) in the **Nakoba** community lab thread.

---

*Nakoba Hands-on Labs. Based on Microsoft Learn's open-source exercises ([mslearn-genaiops](https://github.com/MicrosoftLearning/mslearn-genaiops), [mslearn-mlops](https://github.com/MicrosoftLearning/mslearn-mlops)), MIT licence (see [LICENSE](LICENSE)), updated and fixed for classroom use.*
