# MLOps – Share your learnings and clean up

[⬅ Lab 3 – GitHub Actions](04-github-actions.md) | [🏠 Track home](../README.md) | [Next: Troubleshooting ➡](06-troubleshooting.md)

## Share your learnings (before cleaning up)

**Screenshots:**
1. The pipeline graph with both steps green (Lab 1).
2. The RAI dashboard: the error-analysis tree and the feature importances (Lab 2).
3. A green GitHub Actions run, and the pull request showing the passed **train** check (Lab 3).

**LinkedIn post structure** (in your own words):
- **Problem:** manual, one-off ML training doesn't scale, and accuracy alone hides where a model fails.
- **What I did:** built a reusable Azure ML pipeline, created a Responsible AI dashboard (error analysis + interpretability), and automated training with GitHub Actions on every pull request, with branch protection and a scoped service principal.
- **Result / lesson:** e.g. "errors were concentrated in [segment]" or "no change reaches main without a successful training run".
- **Problems I solved:** retired environments, the wrong data columns in the RAI lab, YAML indentation, branch protection approvals.

Use `#AzureMachineLearning #MLOps #ResponsibleAI #GitHubActions #DevOps`, and tag **Nakoba**. Then share your screenshots and one lesson in the **Nakoba** community lab thread.

## Clean up (don't skip)

### 1. Delete the Azure resources (Cloud Shell)

```bash
cd ~/nakoba-labs/mlops/infra
bash cleanup.sh
```
Type the resource group name to confirm. It takes 5–10 minutes.
> *Can't find infra/lab.env*: the script lists your `rg-nakoba-...` groups; run `bash cleanup.sh rg-nakoba-<suffix>`.

**Or in the portal:** **Resource groups** → **rg-nakoba-<suffix>** → **Delete resource group** → type the name → **Delete**.

### 2. Delete the service principal (Lab 3)

```bash
az ad sp list --display-name sp-nakoba-mlops-github --query "[].{name:displayName, id:appId}" -o table
az ad sp delete --id <appId from the table>
```

### 3. GitHub

Your repo → **Settings** → **Secrets and variables** → **Actions** → delete **AZURE_CREDENTIALS** (it no longer works anyway). You can keep the repo: it shows your work.

### Check
- [ ] **Resource groups** no longer lists `rg-nakoba-<suffix>`
- [ ] Tomorrow, **Cost Management → Cost analysis** shows no new charges

[⬅ Lab 3 – GitHub Actions](04-github-actions.md) | [🏠 Track home](../README.md) | [Next: Troubleshooting ➡](06-troubleshooting.md)
