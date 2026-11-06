# MLOps Setup – Provision the workspace and clone the labs

[⬅ Overview](00-overview.md) | [🏠 Track home](../README.md) | [Next: Lab 1 – Pipelines ➡](02-run-pipelines.md)

Do this **once** for all three MLOps labs. **Time:** 15–20 minutes.

## Prerequisites

| You need | Why |
|---|---|
| Azure subscription where you're **Owner** or **Contributor** (Free Trial works) | To create the workspace and compute |
| **Edge** or **Chrome** | The portal and studio work best there |
| For Lab 3 only: a **GitHub account**, plus **VS Code and Git** on your computer | To run the workflow from your own repo ([install guide](../../genaiops/docs/00-prerequisites.md)) |

**Recommended:** set a budget alert. Portal search bar → **Budgets** → **+ Add** → amount `5` → alert at `80`% to your email → **Create**.

**Check quota:** portal search **Quotas** → **Machine learning** → your region (*East US* by default) → *Standard DSv2 Family Cluster Dedicated vCPUs*. You need **at least 4** free. Free Trial has 4: that works, because the setup script then uses a 1-node cluster.

## 1. Open Cloud Shell

1. Go to https://portal.azure.com.
2. Click the **[>_] Cloud Shell** icon (top bar, right of the search box).
3. Choose **Bash**. (In PowerShell? Click **Switch to Bash**.)
4. If asked about storage: **No storage account required** → your subscription → **Apply**.

> Options don't appear and Cloud Shell won't start? Cloud Shell **Settings** (⚙) → **Reset user settings**, then open it again.

## 2. Clone the repo and run the setup script

Paste with **Shift+Insert** (or right-click → **Paste**) and press **Enter**:

```bash
cd ~
rm -rf nakoba-labs
git clone https://github.com/SHADRACK-NAKOBA/nakoba-genaiops-mlops-labs.git nakoba-labs
cd nakoba-labs/mlops/infra
bash setup.sh
```

> **In a class?** Each person needs their own suffix (4–18 letters/numbers): `bash setup.sh jane2026`. Another region: `bash setup.sh jane2026 westeurope`.

It takes **8–12 minutes**. Messages about installing extensions are normal. It ends with:

```
 DONE. Write these names down:
   Resource group:    rg-nakoba-<suffix>
   Workspace:         mlw-nakoba-<suffix>
   Compute instance:  ci<suffix>
   Compute cluster:   aml-cluster
```

The names are also saved in `~/nakoba-labs/mlops/infra/lab.env`. The script is **safe to run again** (it reuses your suffix and skips what exists).

> ❌ Error? See [Troubleshooting](06-troubleshooting.md) T1–T5 (T5 creates everything in the portal instead).

## 3. Open the studio and check the compute

1. Portal search bar: type **`mlw-nakoba`** → click your workspace → **Launch studio**. Close any pop-ups.
2. Left menu **Compute**:
   - **Compute instances:** `ci<suffix>` is **Running** (if *Stopped*, tick it → **Start**).
   - **Compute clusters:** `aml-cluster` is **Succeeded** with **0** nodes (nodes only start for jobs).

## 4. Clone the labs onto the compute instance

1. **Compute instances** tab → in your instance's **Applications** column, click **Terminal**.
2. Paste (**Ctrl+Shift+V**) and press **Enter**:
   ```bash
   cd ~/cloudfiles/code/Users/*/
   git clone https://github.com/SHADRACK-NAKOBA/nakoba-genaiops-mlops-labs.git nakoba-labs
   ```
   > You **don't** need `pip install` here: each notebook installs what it needs into its own kernel.
3. Left menu **Notebooks** → **Files** pane → **↻ Refresh**. You'll see **nakoba-labs/mlops/notebooks** with:
   - `01-run-pipeline-job.ipynb` (Lab 1)
   - `02-responsible-ai-dashboard.ipynb` (Lab 2)
   - `lab_helpers.py`

## How to run a notebook (both labs)

1. Click the notebook to open it.
2. Top right: **Compute** = your instance (green dot); **kernel** = **Python 3.10 - SDK v2** (on some instances it's called **Python 3.10 - AzureML**). Never *Python 3.8*.
3. A blue **Authenticate** banner? Click it and sign in.
4. Run the cells one by one with **Shift+Enter** (or **▷▷ Run all**).
5. If the first cell says *"you may need to restart the kernel"*: click **⟳ Restart**, then continue from the **second** cell.

[⬅ Overview](00-overview.md) | [🏠 Track home](../README.md) | [Next: Lab 1 – Pipelines ➡](02-run-pipelines.md)
