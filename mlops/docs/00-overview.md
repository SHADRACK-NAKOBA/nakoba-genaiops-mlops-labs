# MLOps Track – Overview and key concepts

[🏠 Track home](../README.md) | [Next: Provision the workspace ➡](01-provision-workspace.md)

Three labs on one Azure Machine Learning workspace, with one setup and one clean-up:

| Lab | Scenario | You learn |
|---|---|---|
| **1. Run pipelines** | Turn *prepare data → train model* into a reusable, repeatable **pipeline** | Components, pipeline jobs, outputs, monitoring in the studio |
| **2. Responsible AI dashboard** | Accuracy isn't enough: find **where** the model fails and **why** it predicts what it does | RAI components, error analysis, feature importance, cohorts |
| **3. Automate training with GitHub Actions** | Make training part of the development workflow: run on demand and on every pull request | Service principal, GitHub secrets/variables, workflows, branch protection, PR-triggered training |

**Dataset:** 10,000 diabetes patients, 8 medical features, target `Diabetic` (1/0).

```
 Cloud Shell                       Azure ML workspace  mlw-nakoba-<suffix>
 ───────────                       ───────────────────────────────────────
 mlops/infra/setup.sh ──creates──► Compute instance ci<suffix>   (notebooks)
                                   Compute cluster  aml-cluster  (pipelines + jobs)
                                   Data assets      diabetes-data, diabetes-training

 Lab 1  notebooks/01-run-pipeline-job        ──► pipeline: prep_data → train_model
 Lab 2  notebooks/02-responsible-ai-dashboard ──► RAI pipeline → dashboard on the model
 Lab 3  .github/workflows/manual-trigger-job  ──► GitHub runner ──az ml job create──► command job
```

## Key concepts

| Concept | What it is |
|---|---|
| **Workspace** | Central place for data, compute, jobs, models and pipelines |
| **Compute instance** | Your cloud workstation for notebooks and the terminal (bills while running) |
| **Compute cluster** | VMs that start for jobs and scale back to 0 (bills only while jobs run) |
| **Component** | A reusable step: a script plus its inputs, outputs and environment |
| **Pipeline job** | Steps linked by their inputs/outputs, run as one job |
| **Responsible AI dashboard** | One view of error analysis, model overview, data analysis and feature importance |
| **Error analysis** | Finds the data segments (cohorts) where the model makes most mistakes |
| **Interpretability** | Explains which features drive predictions, overall and for one prediction |
| **Service principal** | An identity for automation: lets GitHub sign in to Azure without your password |
| **GitHub secrets / variables** | Encrypted (secret) or plain (variable) values a workflow can read |
| **Branch protection** | Rules that stop direct pushes to `main` and require pull requests or passing checks |

## Cost

**About US $0.50–$3** for all three labs if you clean up at the end. The compute instance bills while it's running (it auto-stops after 60 idle minutes); cluster nodes bill only during jobs. GitHub Actions minutes are free for public repos. Pricing: https://azure.microsoft.com/en-us/pricing/details/machine-learning/

## Documentation

- Azure Machine Learning: https://learn.microsoft.com/en-us/azure/machine-learning/
- Pipelines: https://learn.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines
- Responsible AI dashboard: https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai-dashboard
- Create a Responsible AI dashboard (SDK/CLI): https://learn.microsoft.com/en-us/azure/machine-learning/how-to-responsible-ai-insights-sdk-cli
- GitHub Actions: https://docs.github.com/en/actions/get-started/quickstart
- Secrets: https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- Branch protection: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule

[🏠 Track home](../README.md) | [Next: Provision the workspace ➡](01-provision-workspace.md)
