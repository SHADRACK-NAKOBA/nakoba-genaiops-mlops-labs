# MLOps Lab 2 – Create and explore the Responsible AI dashboard

[⬅ Lab 1 – Pipelines](02-run-pipelines.md) | [🏠 Track home](../README.md) | [Next: Lab 3 – GitHub Actions ➡](04-github-actions.md)

**Scenario.** You have a trained diabetes model. Before anyone relies on it, you want to know more than its accuracy: **where** does it make mistakes, **which** features drive its predictions, and does it behave differently across **groups** of patients?

**Time:** about 40 minutes (15–25 of it waiting). **Cost:** cents.

| RAI component | Answers |
|---|---|
| `rai_tabular_insight_constructor` | Sets up the analysis: model + train/test data + target column |
| `rai_tabular_erroranalysis` | *Where* does the model fail? (error tree and heat map) |
| `rai_tabular_explanation` | *Why* does it predict that? (feature importance) |
| `rai_tabular_insight_gather` | Combines everything into one dashboard |

## 1. Run the notebook

1. Studio → **Notebooks** → **nakoba-labs → mlops → notebooks → 02-responsible-ai-dashboard.ipynb**.
2. Kernel **Python 3.10 - SDK v2**. Run the cells in order:

| Cell | What happens | You should see |
|---|---|---|
| `%pip install ...` | SDK, pyarrow, pandas | Restart if asked |
| Prepare the data | Converts the train (10,000 rows) and test (5,000 rows) CSV files to Parquet, without any ID column | `train: (10000, 9), test: (5000, 9)` and a table |
| Connect | Workspace + cluster check | `Connected to workspace: ...` |
| Register data | Creates `diabetes_train_mltable` and `diabetes_test_mltable` (version 1) | `Created data asset ...` (or `Found ...` on a re-run) |
| Registry | Connects to Microsoft's **azureml** registry | The registry client |
| Register model | Registers the MLflow model in **model/** as `local-mlflow-diabetes` | `Registered model: local-mlflow-diabetes:1` |
| Get components | The 4 built-in RAI components, all the same version | `RAI components version: 0.xx.x` |
| Build pipeline + inputs + output | Constructor → error analysis + explanations → gather | (no output) |
| **Submit and wait** | Runs the pipeline and prints the status every 30 seconds | A link, then `Latest status: Running` ... `Completed` |

> The last cell keeps running until the pipeline finishes (**15–25 minutes**). That's expected: don't stop it. Click the link to watch the graph meanwhile.

## 2. Open the dashboard

1. Studio → left menu **Models** → **local-mlflow-diabetes** → click the **version** you registered.
2. **Responsible AI** tab → click **RAI dashboard diabetes**.
3. At the top, under **Connect to compute**, select your **compute instance** (some views need it to recalculate). Wait until it says connected.

> The dashboard isn't there? Check the pipeline is **Completed** (all steps green), click **↻ Refresh**, and make sure you opened the **same model version** the notebook printed.

## 3. Explore it

| View | What to do | What to look for |
|---|---|---|
| **Error analysis** (tree map) | Hover over the nodes; the redder the node, the higher its error rate | Segments with far more errors than the average, e.g. a *PlasmaGlucose* or *Age* range |
| **Error analysis** → **Heat map** | Choose 1–2 features (e.g. *Age*, *BMI*) | Combinations where errors cluster |
| **Model overview** | Check accuracy, precision, recall; click **+ New cohort** to make a group (e.g. *Age > 50*) | Does performance differ between cohorts? |
| **Data analysis** | **Table view** / **Chart view** | Class balance (how many diabetic vs not), feature distributions |
| **Feature importances** → **Aggregate** | Top features overall | Which features the model relies on most |
| **Feature importances** → **Individual** | Pick one patient | Why the model predicted what it did for that person |

**Discuss with your group:**
- Are errors spread evenly, or concentrated in one segment? Who could be harmed by those errors?
- Do the most important features make medical sense?
- What would you do next: collect more data for that segment, try another algorithm, add a human review, or change the decision threshold?

## ✅ Check

- [ ] The RAI pipeline **Completed**
- [ ] You opened the dashboard and connected it to compute
- [ ] You can name the segment with the highest error rate and the top 3 features

[⬅ Lab 1 – Pipelines](02-run-pipelines.md) | [🏠 Track home](../README.md) | [Next: Lab 3 – GitHub Actions ➡](04-github-actions.md)
