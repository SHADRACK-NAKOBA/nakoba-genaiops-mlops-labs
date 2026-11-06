# MLOps Lab 1 – Run pipelines in Azure Machine Learning

[⬅ Provision](01-provision-workspace.md) | [🏠 Track home](../README.md) | [Next: Lab 2 – Responsible AI ➡](03-responsible-ai-dashboard.md)

**Scenario.** A developer wants training to be **repeatable and modular**: the same data preparation and training steps every time, on scalable compute, tracked in one place. You build a 2-step **pipeline** from reusable **components** and run it on the compute cluster.

**Time:** about 30 minutes (15–20 of it waiting for the pipeline). **Cost:** cents.

## 1. Run the notebook

1. Studio → **Notebooks** → **nakoba-labs → mlops → notebooks → 01-run-pipeline-job.ipynb**.
2. Check compute and kernel (**Python 3.10 - SDK v2**), as in the [setup guide](01-provision-workspace.md#how-to-run-a-notebook-both-labs).
3. Run the cells in order (**Shift+Enter**):

| Cell | What happens | You should see |
|---|---|---|
| `%pip install ...` | SDK into this kernel | Quiet finish (restart if asked) |
| Connect + checks | Workspace, `aml-cluster` and `diabetes-data` (creates them if missing) | `Connected to workspace: mlw-nakoba-...` and `found` lines |
| `src` + 2× `%%writefile` | Writes **prep-data.py** (drop missing values, normalise) and **train-model.py** (logistic regression, saved as an MLflow model) | `Writing src/prep-data.py`, `Writing src/train-model.py` |
| Define the components | Picks a current scikit-learn environment and writes **prep-data.yml** and **train-model.yml** | Both YAML files printed |
| `load_component` | Turns the YAML files into components | (no output) |
| `@pipeline` | Links them: the output of *prep_data* becomes the input of *train_model* | The pipeline definition |
| Settings | Upload outputs, run on `aml-cluster`, store in `workspaceblobstore` | The updated definition |
| Submit | Sends the pipeline to the workspace | `Pipeline job name: ...` and `Monitor it at: https://ml.azure.com/...` |

## 2. Watch it run (15–20 minutes)

1. Click the **Monitor it at** link (or **Jobs** → **pipeline_diabetes** → your job).
2. The **graph** shows *Prepare training data* → *Train a logistic regression model*. Each step goes **Queued → Running → Completed** (green).
   - *Queued* for 5 minutes is normal: the cluster is starting a node.
   - The first run takes longer because the environment image has to be pulled.

## 3. Explore the results

| Where | What to look at |
|---|---|
| Click **Prepare training data** → **Outputs + logs** → `user_logs/std_log.txt` | `Preparing 10000 rows of data` |
| Click **Train a logistic regression model** → **Metrics** | Training metrics autologged by MLflow |
| Same step → **Outputs + logs** → `user_logs/std_log.txt` | `Accuracy: ...` and `AUC: ...` (about 0.77 and 0.85) |
| Same step → **Outputs + logs** → *model_output* | The saved MLflow model (`MLmodel`, `model.pkl`) |
| Pipeline **Overview** | Inputs, outputs and duration of the whole run |

> 💡 **Why pipelines?** Each step can be re-run, reused in other pipelines, scheduled, and given its own compute. If only the training code changes, the data step can be reused instead of re-running.

## ✅ Check

- [ ] The pipeline job is **Completed** with 2 green steps
- [ ] You found the accuracy in the training step's log
- [ ] You can explain how the output of one component becomes the input of the next

[⬅ Provision](01-provision-workspace.md) | [🏠 Track home](../README.md) | [Next: Lab 2 – Responsible AI ➡](03-responsible-ai-dashboard.md)
