# MLOps – Interview questions from these labs

[🏠 Track home](../README.md)

**60-second pitch:** "On Azure Machine Learning I built a two-step training pipeline from reusable components, so data preparation and training are repeatable and run on a scalable cluster. Before trusting the model, I generated a Responsible AI dashboard with error analysis and feature importance, to see which patient segments it fails on and why. Then I automated training with GitHub Actions: a scoped service principal stored as a secret, a workflow that submits the Azure ML job on demand and on every pull request, and branch protection so nothing reaches main without a successful training run."

| Question | Strong answer |
|---|---|
| Why pipelines instead of one script? | Modular, reusable steps; each step's inputs/outputs are tracked; steps can be cached, scheduled, re-run and put on different compute; easier to test and to hand over. |
| What's a component? | A self-contained step: code, inputs, outputs, environment and command, defined once (YAML/SDK) and reused in many pipelines. |
| Why is accuracy not enough? | An overall number hides **where** errors happen. A model can be 80% accurate overall and much worse for one group. Error analysis and cohorts show that; feature importance shows if the model relies on sensible signals. |
| What did the RAI dashboard show you? | Name the segment with the highest error rate and the top features. Then say what you'd do: more data for that cohort, a different model, a threshold change, or human review. |
| Global vs local explanations? | Global (aggregate) = which features matter overall. Local (individual) = why the model made **this** prediction for **this** person. |
| Why a service principal, and how did you limit it? | Automation needs an identity that isn't a person's password. Scoped to **Contributor on one resource group**, stored as an encrypted GitHub secret. In production: OIDC (federated credentials, no secret), least-privilege roles and secret rotation. |
| Secret vs variable in GitHub? | Secrets are encrypted and masked in logs (credentials). Variables are plain configuration (resource group, workspace name). |
| Why run training on pull requests? | Every proposed change is validated before merge. A broken training script or bad parameter fails the check, not production. |
| What does branch protection add? | No direct pushes to main; changes go through PRs; required status checks must pass. In a team, required reviews too. |
| How would you secure this for production? | Private endpoints and no public access on the workspace, self-hosted runners in the VNet, OIDC instead of a client secret, environments with approvals for prod, and separate dev/prod workspaces. |
| What went wrong, and how did you fix it? | Example: the original RAI lab fed the model a `PatientID` column it was never trained on, and wrote to a folder that didn't exist. I used data with exactly the model's 8 features and fixed the paths. Or: a curated environment had been retired, so I switched to the current scikit-learn environment. |

[🏠 Track home](../README.md)
