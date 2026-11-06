# MLOps Lab 3 – Automate model training with GitHub Actions

[⬅ Lab 2 – Responsible AI](03-responsible-ai-dashboard.md) | [🏠 Track home](../README.md) | [Next: Share and clean up ➡](05-share-and-cleanup.md)

**Scenario.** Your team wants every training run to be consistent and part of the development workflow: start training **on demand** from GitHub, and **automatically on every pull request**, so no change reaches `main` without a successful training run.

**Time:** about 60 minutes. **Cost:** cents (GitHub Actions is free for public repos).

```
 your GitHub repo ──(Run workflow / pull request)──► GitHub runner
                                                       │ azure/login (service principal from the AZURE_CREDENTIALS secret)
                                                       ▼
                                   az ml job create -f mlops/src/job.yml ──► Azure ML command job on aml-cluster
```

## Before you start

- [MLOps setup](01-provision-workspace.md) done: the workspace, `aml-cluster` and the **diabetes-data** data asset exist.
- **Your own copy** of this repo on GitHub, cloned in VS Code on your computer. Already done it for the GenAIOps track? Use the same one. If not:
  1. Open **https://github.com/SHADRACK-NAKOBA/nakoba-genaiops-mlops-labs** → **Use this template** → **Create a new repository** (no button? **Fork**).
  2. **Owner:** you, **Name:** `nakoba-genaiops-mlops-labs`, **Public** (branch protection on free accounts needs a public repo) → **Create repository**.
  3. VS Code → **Ctrl+Shift+P** → **Git: Clone** → `https://github.com/<you>/nakoba-genaiops-mlops-labs.git` → choose a folder → **Open**.

## 1. Turn on Actions in your repo

Your repo on GitHub → **Actions** tab. If you see *Workflows aren't being run on this forked repository*, click **I understand my workflows, go ahead and enable them**. You'll see the workflow **Manually trigger an Azure Machine Learning job**.

## 2. Create the service principal (Cloud Shell)

A **service principal** is an identity for automation, so GitHub can sign in to Azure without your password. It only gets **Contributor** on your lab resource group.

1. Portal → **Cloud Shell** (**Bash**). Check the subscription: `az account show --query name -o tsv`.
2. Run:
   ```bash
   cd ~/nakoba-labs/mlops/infra
   bash create-github-sp.sh
   ```
   > *No such file or directory*? Cloud Shell was reset: clone again ([setup step 2](01-provision-workspace.md#2-clone-the-repo-and-run-the-setup-script)), then run `bash create-github-sp.sh rg-nakoba-<suffix> mlw-nakoba-<suffix>`.
3. It prints **1. a JSON block** (the secret) and **2. two values** (the variables). Keep the Cloud Shell open.

> ⚠️ The JSON contains a password (`clientSecret`). Never commit it or paste it anywhere except the GitHub secret.

## 3. Add the secret and variables to GitHub

Your repo → **Settings** → left menu **Secrets and variables** → **Actions**.

1. **Secrets** tab → **New repository secret**:
   - **Name:** `AZURE_CREDENTIALS`
   - **Secret:** paste the whole JSON, from `{` to `}` → **Add secret**.
2. **Variables** tab → **New repository variable**:
   - **Name:** `AZURE_RESOURCE_GROUP` · **Value:** `rg-nakoba-<suffix>` → **Add variable**
3. **New repository variable** again:
   - **Name:** `AZURE_WORKSPACE_NAME` · **Value:** `mlw-nakoba-<suffix>` → **Add variable**

Names must be **exactly** as above (capital letters, underscores).

## 4. Review the workspace's network access (read only)

Portal → your workspace **mlw-nakoba-<suffix>** → **Settings** → **Networking**. Look at **Public access** and **Private endpoint connections**:
- **All networks** (the default) lets GitHub-hosted runners reach the workspace: **keep it for this lab**.
- In production you'd usually disable public access, use **private endpoints**, and run workflows on **self-hosted runners** inside the network, combined with RBAC.

## 5. Review the training job definition

In VS Code open **mlops/src/job.yml**. It's ready to use:

```yaml
inputs:
  training_data:
    type: uri_file
    path: azureml:diabetes-data@latest      # data asset created by setup.sh
  reg_rate: 0.01
environment: azureml://registries/azureml/environments/sklearn-1.5/labels/latest
compute: azureml:aml-cluster
```

It runs **mlops/src/train-model-parameters.py**, which logs *Accuracy* and *AUC* with MLflow.

## 6. Add the training step to the workflow

1. In VS Code open **.github/workflows/manual-trigger-job.yml**.
2. At the **end** of the file, add this step. It must line up exactly with the other `- name:` lines (**4 spaces** before `-`):
   ```yaml
       - name: Run Azure Machine Learning training job
         run: az ml job create -f mlops/src/job.yml --stream --resource-group ${{ vars.AZURE_RESOURCE_GROUP }} --workspace-name ${{ vars.AZURE_WORKSPACE_NAME }}
   ```
   > YAML is strict about spaces. Not sure? Copy the finished file **mlops/solutions/manual-trigger-job.yml** over it (that version also has the pull-request trigger from step 9, which is fine).
3. Save (**Ctrl+S**), then commit and push. In VS Code's terminal (repo root):
   ```bash
   git add .github/workflows/manual-trigger-job.yml
   git commit -m "Add Azure ML training job step"
   git push origin main
   ```

## 7. Run the workflow manually

1. GitHub → **Actions** → **Manually trigger an Azure Machine Learning job** → **Run workflow** → branch **main** → **Run workflow**.
2. Refresh after a few seconds → click the run → click **train** to watch the steps live.
3. **Run Azure Machine Learning training job** streams the job's log. It takes **10–15 minutes** and ends with a green ✔.

> ❌ Red step? Click it and read the error ([Troubleshooting T10](06-troubleshooting.md#t10-github-actions-workflow-fails)). Most common: wrong secret JSON, a variable name typo, or the data asset missing.

## 8. Check the job in Azure ML

Studio → **Jobs** → **diabetes-training** → the newest **diabetes-train-command** job:
- **Overview:** the inputs (`diabetes-data`, `reg_rate 0.01`)
- **Metrics:** *Accuracy* and *AUC*
- **Outputs + logs:** `user_logs/std_log.txt` and the `metrics_output` folder

🎉 Training now runs from GitHub on demand.

## 9. Trigger training on pull requests

1. In **manual-trigger-job.yml**, change the `on:` section to:
   ```yaml
   on:
     workflow_dispatch:
     pull_request:
       branches:
         - main
   ```
2. Commit and push to main:
   ```bash
   git add .github/workflows/manual-trigger-job.yml
   git commit -m "Run training on pull requests to main"
   git push origin main
   ```

## 10. Protect the main branch

GitHub → your repo → **Settings** → **Branches** → **Add classic branch protection rule** (or **Add branch protection rule**):

1. **Branch name pattern:** `main`
2. Tick **Require a pull request before merging**.
   - ⚠️ Then **untick** **Require approvals**. You can't approve your own pull request, so leaving it ticked would block you from merging.
3. (Recommended) Tick **Require status checks to pass before merging** → search for **train** and select it. (It appears after the workflow has run at least once.)
4. Click **Create** (scroll to the bottom) and confirm with your password if asked.

> Prefer *Rulesets*? **Settings → Rules → Rulesets → New branch ruleset**, target `main`, tick **Require a pull request before merging** (0 approvals) → **Create**. Either works.

## 11. Make a change on a feature branch

In VS Code's terminal (repo root):

```bash
git checkout main
git pull
git checkout -b feature/update-parameters
```

Open **mlops/src/job.yml** and change `reg_rate: 0.01` to **`reg_rate: 0.02`**. Save, then:

```bash
git add mlops/src/job.yml
git commit -m "Adjust training parameters"
git push --set-upstream origin feature/update-parameters
```

## 12. Open a pull request and watch training run

1. GitHub shows a yellow banner: **feature/update-parameters had recent pushes** → **Compare & pull request**. (No banner? **Pull requests** → **New pull request** → base **main** ← compare **feature/update-parameters**.)
2. Check that the base is **your** repo's `main` (for forks, GitHub sometimes picks the original repo: change it), then **Create pull request**.
3. At the bottom of the PR, **Manually trigger an Azure Machine Learning job / train** starts automatically ⏳.
4. When it shows a green ✔ (10–15 minutes), click **Merge pull request** → **Confirm merge** → **Delete branch**.
5. Back in VS Code:
   ```bash
   git checkout main
   git pull
   ```

Studio → **Jobs** → **diabetes-training** now has a job with **reg_rate 0.02**. Compare its *Accuracy* with the first run.

## ✅ Check

- [ ] The manual workflow run succeeded and its job is in the studio
- [ ] `main` is protected: direct pushes need a PR
- [ ] A pull request triggered training automatically, and you merged it after it passed

> Doing the GenAIOps track after this? `main` is now protected, so push your GenAIOps work through a branch and PR, or temporarily turn off the rule.

[⬅ Lab 2 – Responsible AI](03-responsible-ai-dashboard.md) | [🏠 Track home](../README.md) | [Next: Share and clean up ➡](05-share-and-cleanup.md)
