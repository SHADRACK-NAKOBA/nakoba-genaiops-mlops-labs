# GenAIOps Lab 1 setup – Create your repo and deploy Microsoft Foundry

[⬅ Prerequisites](00-prerequisites.md) | [🏠 Track home](../README.md) | [Next: Prompt and agent versions ➡](02-prompt-and-agent-versions.md)

Do this **once**. Labs 2 and 3 both use what you create here. **Time:** about 20 minutes.

## 1. Create your own copy of the repo

You'll commit, tag and branch, so you need a repo that **you** own.

1. Sign in to GitHub and open **https://github.com/SHADRACK-NAKOBA/nakoba-genaiops-mlops-labs**.
2. Click the green **Use this template** button → **Create a new repository**.
   > No *Use this template* button? Click **Fork** → **Create fork** instead. Everything else is the same.
3. **Owner:** your account. **Repository name:** `nakoba-genaiops-mlops-labs`. Choose **Public** (needed later for branch protection in the MLOps track) → **Create repository**.

## 2. Clone it in VS Code

1. Open VS Code. Press **Ctrl+Shift+P** (Mac: **Cmd+Shift+P**), type **Git: Clone**, press **Enter**.
2. Paste **your** repo URL: `https://github.com/<your-username>/nakoba-genaiops-mlops-labs.git` → **Enter**.
3. Pick a folder (e.g. *Documents*) → **Select as Repository Destination**.
4. Click **Open** when asked. If asked *Do you trust the authors?* click **Yes, I trust the authors**.

## 3. Open a terminal in the genaiops folder

Menu **Terminal → New Terminal**, then:

```bash
cd genaiops
```

> **Every command in the GenAIOps labs runs from this `genaiops` folder** (the terminal prompt ends in `...\nakoba-genaiops-mlops-labs\genaiops>`). If a command says *file not found*, run `cd genaiops` first.

## 4. Sign in to Azure (twice: azd and az)

```bash
azd auth login
```
A browser opens → pick your account → close the tab when it says you're signed in.

```bash
az login
```
Sign in again in the browser. If several subscriptions are listed, type the **number** of the one to use and press **Enter**.

> **The terminal freezes or closes during sign-in?** Use the code method instead: `az login --use-device-code` and `azd auth login --use-device-code`, then open the link shown and type the code. (Don't use `--username/--password`: it doesn't work with multi-factor sign-in, which Azure now requires.)

## 5. Deploy the Foundry resources

```bash
azd up
```

Answer the questions (use the arrow keys and **Enter**):

| Question | Answer |
|---|---|
| **Enter a unique environment name** | e.g. `nakoba-jane` (letters, numbers, hyphens). It's used in every resource name. |
| **Select an Azure Subscription** | Your subscription |
| **Select an Azure location** | **Sweden Central** (or **East US 2**) |

Wait **5–10 minutes**. It creates:

| Resource | Purpose |
|---|---|
| Resource group `rg-<env-name>` | Holds everything; delete it to stop all costs |
| **Foundry** resource (AI Services) | Hosts the models |
| **Foundry project** `ai-project-<env-name>` | Where your agents live |
| Model deployments **`gpt-5.1`** and **`gpt-5-mini`** | The two models the labs use |
| Log Analytics + Application Insights | Monitoring |
| Role assignments for **you** | So your Python scripts may create agents |

Expected end: `SUCCESS: Your up workflow to provision and deploy to Azure completed`.

> ❌ **Error** (quota, region, *InsufficientQuota*, *InvalidTemplateDeployment*)? See [Troubleshooting](06-troubleshooting.md) T3–T5.

## 6. Create the .env file

```bash
python scripts/make_env.py
```

Expected:
```
Wrote ...\genaiops\.env (... values, UTF-8)
  AZURE_AI_PROJECT_ENDPOINT = https://....services.ai.azure.com/api/projects/ai-project-<env>
  AGENT_NAME = trail-guide   MODEL_NAME = gpt-5.1
```

> 💡 This replaces `azd env get-values > .env`. In Windows PowerShell that command saves the file in UTF-16, which Python can't read. The script always writes UTF-8 and adds `AGENT_NAME` and `MODEL_NAME` for you. Never commit `.env` (it's already in `.gitignore`).

## 7. Create the Python virtual environment

**Windows (PowerShell, the VS Code default):**
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.venv\Scripts\Activate.ps1
```

**macOS / Linux / Git Bash:**
```bash
python3 -m venv .venv
source .venv/bin/activate        # Git Bash on Windows: source .venv/Scripts/activate
```

Your prompt now starts with **(.venv)**. Then:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> The `Set-ExecutionPolicy` line fixes *"running scripts is disabled on this system"*. It only applies to this terminal. **Every time you open a new terminal**, run `cd genaiops`, then the activate lines again.

## ✅ Check

```bash
python -c "import azure.ai.projects, dotenv; print('SDK', azure.ai.projects.__version__, 'ready')"
```
Should print `SDK 2.10.0 ready`.

- [ ] Your own repo exists on GitHub and is open in VS Code
- [ ] `azd up` succeeded
- [ ] `.env` created by `make_env.py`
- [ ] `(.venv)` active and requirements installed

[⬅ Prerequisites](00-prerequisites.md) | [🏠 Track home](../README.md) | [Next: Prompt and agent versions ➡](02-prompt-and-agent-versions.md)
