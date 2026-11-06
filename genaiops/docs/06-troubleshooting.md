# GenAIOps – Troubleshooting

[🏠 Track home](../README.md)

Read the **last red line** of the error first: it usually names the problem.

### T1. `'python' / 'az' / 'azd' is not recognized` or `command not found`
Close **every** VS Code and terminal window and open a new one (new installs only show up in new windows). Still failing? Restart the computer. Python opens the Microsoft Store? See [prerequisites B2.4](00-prerequisites.md#b2-python).

### T2. `running scripts is disabled on this system` (activating .venv)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.venv\Scripts\Activate.ps1
```
Run both lines in every new PowerShell terminal. (Permanent alternative: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.)

### T3. `azd up`: *InsufficientQuota* / *quota exceeded* for gpt-5.1 or gpt-5-mini
Your subscription doesn't have enough model quota in that region.
- **Lower the capacity:** open `infra/main.bicep`, change both `"capacity": 20` to `"capacity": 10`, save, run `azd up` again.
- **Another region:** `azd down --purge`, then `azd env new <new-name>`, then `azd up` and choose **East US 2** or **Sweden Central** (whichever you didn't try).
- **Check your quota:** https://ai.azure.com → **Management center** (or **Operate**) → **Quota** → filter by model.

### T4. `azd up`: *model ... not available in this region* / *DeploymentModelNotSupported*
Pick **Sweden Central** or **East US 2**: `azd down --purge`, `azd env new <new-name>`, `azd up`.

### T5. `azd up`: *subscription is not registered* / *MissingSubscriptionRegistration*
```bash
az provider register --namespace Microsoft.CognitiveServices --wait
az provider register --namespace Microsoft.OperationalInsights --wait
az provider register --namespace Microsoft.Insights --wait
```
Then run `azd up` again. *AuthorizationFailed*? You need **Owner** (or *Contributor + User Access Administrator*) on the subscription, because `azd up` creates role assignments.

### T6. `PermissionDenied` or `401` when running a script
- Right after `azd up`, role assignments can take **up to 10 minutes**. Wait and run again.
- Check you're signed in to the **same** subscription you deployed to: `az account show`. Wrong one? `az account set --subscription "<name or id>"`.
- Still failing after 15 minutes: `az login` again, then retry.

### T7. `KeyError: 'AZURE_AI_PROJECT_ENDPOINT'`, `.env not found`, or strange characters in .env
You made `.env` with `azd env get-values > .env` (PowerShell saves it as UTF-16). Delete it and run:
```bash
python scripts/make_env.py
```

### T8. `DefaultAzureCredential failed to retrieve a token`
Run `az login` in the **same** terminal, then retry. Behind a company proxy? Try another network.

### T9. Agent creation fails: *deployment not found* / *model not found*
The model name must match a deployment: `gpt-5.1` or `gpt-5-mini`. Check `MODEL_NAME` in `.env` and the `model=` line in `trail_guide_agent.py`. Old tutorials say `gpt-4.1`, but new subscriptions can no longer deploy it (deprecated).

### T10. `ModuleNotFoundError: No module named 'azure'` / `'dotenv'`
The virtual environment isn't active (no **(.venv)** at the start of the prompt). Activate it ([setup step 7](01-setup-foundry.md#7-create-the-python-virtual-environment)) and, if needed, `python -m pip install -r requirements.txt`.

### T11. `can't open file ... trail_guide_agent.py`: No such file
You're not in the genaiops folder. `cd genaiops` (from the repo root), then run the command again.

### T12. `run_batch_tests.py`: *agent 'trail-guide' not found*
Create the agent first: `python src/agents/trail_guide_agent/trail_guide_agent.py`. If you changed `AGENT_NAME` in `.env`, keep it the same for both scripts.

### T13. Rate limit / `429 Too Many Requests` during batch tests
The script retries automatically. If it still stops, wait a minute and rerun it, or raise the capacity (T3, but upwards) if you have quota.

### T14. Git problems
| Message | Fix |
|---|---|
| `nothing to commit, working tree clean` | The file already had that change. Continue. |
| `tag 'v1' already exists` | You ran the step twice. `git tag -f v1` moves it to the current commit. |
| `Please tell me who you are` | Set `git config --global user.name` / `user.email` ([prerequisites](00-prerequisites.md#configure-git-once)). |
| `push ... rejected` / `protected branch` | You turned on branch protection in the MLOps track. Push a branch and open a pull request, or push `main` before turning it on. |
| `Permission ... denied` / `403` on push | You cloned **SHADRACK-NAKOBA**'s repo instead of **your** copy. `git remote set-url origin https://github.com/<you>/nakoba-genaiops-mlops-labs.git` |
| Merge conflict | Open the file, choose the right line (*Accept Current/Incoming*), save, `git add <file>`, `git commit`. |

### T15. The fine-tuning lab page is blank or the buttons don't work
Open `index.html` in **Edge or Chrome** (not inside VS Code's preview). The *Submit selection* button only turns on when exactly **3** cards are selected.

---

Still stuck? Post the **lab and step number** and a screenshot of the **full error** (hide keys and subscription IDs) in the Nakoba community lab thread.

[🏠 Track home](../README.md)
