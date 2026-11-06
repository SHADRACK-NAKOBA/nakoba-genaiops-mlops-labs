# Track 2 – MLOps with Azure Machine Learning

Build a training **pipeline**, check the model with a **Responsible AI dashboard**, and **automate training with GitHub Actions**: all on one Azure Machine Learning workspace.

| # | Step | You learn | Time |
|---|---|---|---|
| 0 | [Overview and key concepts](docs/00-overview.md) | How the three labs fit together | 5 min |
| 1 | [Provision the workspace](docs/01-provision-workspace.md) | `setup.sh` in Cloud Shell, clone onto the compute instance | 20 min |
| 2 | [Lab 1 – Run pipelines](docs/02-run-pipelines.md) | Components, pipeline jobs, outputs | 30 min |
| 3 | [Lab 2 – Responsible AI dashboard](docs/03-responsible-ai-dashboard.md) | Error analysis, interpretability, cohorts | 40 min |
| 4 | [Lab 3 – GitHub Actions](docs/04-github-actions.md) | Service principal, secrets, workflows, PR-triggered training, branch protection | 60 min |
| 5 | [Share and **clean up**](docs/05-share-and-cleanup.md) | LinkedIn post; delete everything | 10 min |
| – | [Troubleshooting](docs/06-troubleshooting.md) | Fixes for every common error | – |
| – | [Interview questions](docs/07-interview-questions.md) | Explain the work in an interview | – |

**Cost:** about US $0.50–$3 for all three labs if you clean up. **Needs:** an Azure subscription (Owner/Contributor; Free Trial works). Lab 3 also needs a GitHub account and VS Code + Git.

```
mlops/
├── infra/
│   ├── setup.sh               ← workspace, compute instance, aml-cluster, data assets
│   ├── create-github-sp.sh    ← service principal + values for GitHub (Lab 3)
│   └── cleanup.sh             ← deletes everything
├── data/
│   ├── diabetes-data/         ← diabetes.csv (10,000 rows) + MLTable
│   └── rai/train-data, rai/test-data   ← data for the RAI dashboard (8 features + Diabetic)
├── model/                     ← trained MLflow model for the RAI dashboard
├── notebooks/
│   ├── 01-run-pipeline-job.ipynb
│   ├── 02-responsible-ai-dashboard.ipynb
│   └── lab_helpers.py         ← connect; create missing cluster/data; pick a current environment
├── src/
│   ├── train-model-parameters.py   ← training script used by GitHub Actions
│   └── job.yml                     ← the Azure ML command job (ready to use)
└── solutions/manual-trigger-job.yml ← finished workflow (the starter is in .github/workflows/)
```

## Fixed compared with the original exercises

| Problem students hit | Fix |
|---|---|
| Labs cloned two different external repos and used different resource names in each lab | One repo, one setup, one set of names (`rg-nakoba-<suffix>`) |
| Portal setup said "give the cluster a **unique name**", then "update the cluster name" in the code | Cluster is always `aml-cluster`; notebooks create a missing cluster and data assets themselves |
| `pip install` in the terminal went into a different Python than the notebook | Each notebook installs its packages with `%pip` |
| Retired **Python 3.8** kernel and retired `AzureML-sklearn-1.0-ubuntu20.04-py38-cpu` environment | Python 3.10 kernel; current `sklearn-1.5` environment chosen automatically |
| RAI notebook (upstream) wrote to a `train-data` folder that doesn't exist, and fed a `PatientID` column the model wasn't trained on | Data folders included; data has exactly the model's 8 features |
| RAI notebook hard-coded model version `:1` (a re-run registers version 2) and crashed with `assert` if the pipeline failed | Uses the version it just registered; prints where to look if it fails |
| GitHub Actions guide: `--scopes/subscriptions` (missing space), `$` instead of `${{ vars... }}`, placeholders in `job.yml` | `create-github-sp.sh` prints the exact secret and variables; `job.yml` is ready; finished workflow in `solutions/` |
| Branch protection with **Require approvals** blocks merging your own PR | Guide says to untick it |
| Free Trial (4 vCPUs) can't fit the instance plus a 2-node cluster | Setup checks quota and uses a 1-node cluster when needed |
| Compute instance billed all night if forgotten | Auto-stops after 60 idle minutes |

*Based on Microsoft Learn's open-source exercises ([MicrosoftLearning/mslearn-mlops](https://github.com/MicrosoftLearning/mslearn-mlops)), updated and fixed for classroom use.*
