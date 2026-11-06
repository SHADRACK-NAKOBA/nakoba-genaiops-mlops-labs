# MLOps – Troubleshooting

[🏠 Track home](../README.md)

Read the **last red line** of the error first.

### T1. setup.sh: "subscription is not registered" or "AuthorizationFailed"
- *not registered*: the script registers the providers itself, so just run `bash setup.sh` again.
- *AuthorizationFailed*: you need **Owner/Contributor** on the subscription, or Cloud Shell is on another subscription: `az account list -o table`, then `az account set --subscription "<name>"`.

### T2. setup.sh: compute instance name "already in use"
Names are unique per region. Start over with your own suffix: `rm -f lab.env`, then `bash setup.sh <yourname><4digits>`. Delete the half-created resource group afterwards.

### T3. Cloud Shell closed or timed out during setup
Open it again and run `cd ~/nakoba-labs/mlops/infra && bash setup.sh` (it skips what exists). Folder gone? Clone again and run `bash setup.sh <your-old-suffix>`.

### T4. Quota errors (`QuotaExceeded`, *not enough quota*)
You need at least 4 free *Standard DSv2 Family* vCPUs.
- Another VM size: `AZ_VM_SIZE=Standard_D2s_v3 bash setup.sh`
- Another region: `bash cleanup.sh`, `rm -f lab.env`, `bash setup.sh <new-suffix> westeurope`
- Stop compute instances from other labs, or **Quotas → Machine learning → Request quota increase**.

### T5. Setup keeps failing: create everything in the portal
1. Portal → **+ Create a resource** → **Azure Machine Learning** → **Create** → **New workspace**. Resource group **`rg-nakoba-labs`** (new), workspace **`mlw-nakoba-labs`**, a region near you, **Container registry: None** → **Review + create** → **Create** → **Launch studio**.
2. **Compute → Compute instances → + New**: a unique name, **Standard_DS11_v2** → **Create**.
3. **Compute clusters → + New**: same region, **Standard_DS11_v2** → **Next** → name exactly **`aml-cluster`**, min 0, max 2 (1 on Free Trial) → **Create**.
4. You **don't** need to upload data: the notebooks create the data assets. For **Lab 3**, run the Lab 1 notebook once first (it creates `diabetes-data`), and use `rg-nakoba-labs` / `mlw-nakoba-labs` as your GitHub variables.

### T6. Notebook kernel, module or sign-in problems
| Symptom | Fix |
|---|---|
| Asks for a kernel / *Python 3.8* | Choose **Python 3.10 - SDK v2** (or **Python 3.10 - AzureML**) |
| `ModuleNotFoundError` (azure.ai.ml, pyarrow) | Run the `%pip` cell, **⟳ Restart**, run again from the second cell |
| `No module named 'lab_helpers'` | Keep the notebook in **mlops/notebooks**, next to `lab_helpers.py` |
| **Authenticate** banner / `DefaultAzureCredential failed` | Click **Authenticate** and sign in, run the cell again |
| `Could not find the workspace configuration` | Run it in the studio's **Notebooks** page on your compute instance, not on your own PC |
| Folder not in the Files pane | **↻ Refresh**; or in the terminal: `cd ~/cloudfiles/code/Users/*/ && git clone https://github.com/SHADRACK-NAKOBA/nakoba-genaiops-mlops-labs.git nakoba-labs` |

### T7. Pipeline (Lab 1) failed
Click the **red** step → **Outputs + logs** → `user_logs/std_log.txt`.
| Message | Fix |
|---|---|
| `Compute target aml-cluster not found` | Run the connect/checks cell again (it creates the cluster), or create it as in T5.3 |
| `diabetes-data ... not found` | Run the checks cell (it creates it) |
| `Environment ... not found` | Re-run the *Define the components* cell (it picks a current environment or builds a fallback) |
| `No such file ... src/prep-data.py` | Run the two `%%writefile` cells before submitting |

### T8. Job stuck in Queued / Preparing
*Queued* up to ~5 minutes (cluster starting) and *Preparing* up to ~10 minutes (first use of an environment) are normal. On a 1-node cluster, jobs also wait for each other. More than 20 minutes: check the job **Overview** for a quota warning (T4).

### T9. Responsible AI pipeline (Lab 2) failed or no dashboard
| Problem | Fix |
|---|---|
| `FileNotFoundError ... train-data` | Run the notebook from **mlops/notebooks** (paths are relative) |
| Constructor step fails with a feature/column mismatch | The data must have only the 8 features + `Diabetic`. Re-run the *Prepare the data* cell (it drops `PatientID`), then re-create the data assets with `data_version = "2"` |
| `ResourceNotFound` for an RAI component | Re-run the *Get the RAI components* cell; check internet access to the azureml registry |
| A step times out (300 s) | Re-submit; if it repeats, change `set_limits(timeout=300)` to `600` for that step |
| No dashboard on the model | The pipeline must be **Completed**; open the model **version** the notebook printed → **Responsible AI** tab → **↻ Refresh** |
| Dashboard says it needs compute | **Connect to compute** at the top → choose your running compute instance |

### T10. GitHub Actions workflow fails
Click the failed run → **train** → the red step.
| Step / message | Fix |
|---|---|
| **Azure login**: `Login failed`, `clientId ... not found`, `AADSTS7000215` | Re-create the secret `AZURE_CREDENTIALS` with the **whole** JSON from `create-github-sp.sh` (from `{` to `}`). If you just created it, wait 2 minutes. |
| **Azure login**: `Not all values are present` | The secret isn't the JSON format above. Run `create-github-sp.sh` again and paste its JSON |
| **Run job**: `argument --resource-group: expected one argument` | A variable is missing or misspelled: `AZURE_RESOURCE_GROUP` and `AZURE_WORKSPACE_NAME` under **Variables** (not Secrets) |
| **Run job**: `AuthorizationFailed` | The service principal was made for another resource group. Re-run `create-github-sp.sh` from the right Cloud Shell |
| **Run job**: `diabetes-data ... not found` | Run `setup.sh` (or the Lab 1 notebook) so the data asset exists |
| **Run job**: `Could not find ... mlops/src/job.yml` | The workflow must run from the repo root: keep `-f mlops/src/job.yml` exactly |
| Workflow file error (red X, *Invalid workflow file*) | YAML indentation. Copy **mlops/solutions/manual-trigger-job.yml** over it, commit, push |
| No **Run workflow** button | The workflow must have `workflow_dispatch:` and be on the **main** branch. Actions disabled? See Lab 3 step 1 |

### T11. create-github-sp.sh: "Insufficient privileges"
Your directory doesn't allow you to create app registrations (common with school or company accounts). Ask your admin, or use a personal Azure account (Free Trial), where you're the admin.

### T12. Branch protection and pull requests
| Problem | Fix |
|---|---|
| *Merging is blocked: Review required* | Edit the rule and **untick Require approvals** (you can't approve your own PR) |
| `push declined due to repository rule violations` / *protected branch* | Expected after Lab 3 step 10: push a branch and open a PR |
| No **train** check offered under *status checks* | Run the workflow once first (step 7), then edit the rule |
| The PR targets SHADRACK-NAKOBA's repo | You forked: change **base repository** to your own repo |
| *Branch protection not available* | The repo is private on a free plan: make it **Public** (Settings → General → Danger zone) |

### T13. git push asks for a password / 403
Use **your** repo: `git remote -v` must show `github.com/<you>/...`. Sign in through the browser window VS Code opens, or install **GitHub CLI** and run `gh auth login`.

---

Still stuck? Post the **lab and step number** and a screenshot of the **full error** (hide secrets and subscription IDs) in the Nakoba community lab thread.

[🏠 Track home](../README.md)
