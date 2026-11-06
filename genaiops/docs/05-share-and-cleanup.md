# GenAIOps – Share your learnings and clean up

[⬅ Fine-tuning](04-fine-tuning.md) | [🏠 Track home](../README.md) | [Next: Troubleshooting ➡](06-troubleshooting.md)

## Share your learnings

Take screenshots **before** you clean up:
1. The **trail-guide** agent in the Foundry portal with its versions.
2. `git log --oneline --decorate` showing the `v1`, `v2`, `v3` and `v4-optimized-prompt` tags.
3. The `compare_experiments.py` table.
4. A fine-tuning scenario with **Score: 3/3 correct**.

**LinkedIn post structure** (in your own words):
- **Problem:** AI agents need to improve without being rebuilt, and changes must be safe, measured and cheap.
- **What I did:** versioned a Microsoft Foundry agent's prompts with Git tags, ran baseline vs experiment branches with batch tests and scoring, compared gpt-5.1 against gpt-5-mini, and chose fine-tuning methods (SFT/DPO/RFT) from evaluation metrics.
- **Result:** e.g. "cut tokens by X% with no quality loss", using **your** numbers.
- **Problems I solved:** retired models, UTF-16 .env files, PowerShell script blocking, role propagation delays.

Use `#MicrosoftFoundry #GenAIOps #PromptEngineering #AIAgents #LLMOps`, and tag **Nakoba**. Then post your screenshots and one lesson learned in the **Nakoba** community lab thread.

## Clean up (don't skip)

From the **genaiops** folder:

```bash
azd down --purge
```

- Type **y** to confirm. It takes 5–15 minutes.
- `--purge` **permanently** deletes the Foundry resource instead of leaving it *soft-deleted* for 48 hours. Without it, the name stays reserved, its model quota stays in use, and a new `azd up` can fail.

Check: portal → **Resource groups** → `rg-<env-name>` is gone.

> `azd down` says *no environment found*? You're not in the genaiops folder (`cd genaiops`), or the `.azure` folder was deleted: delete the resource group in the portal, then **Foundry → Manage deleted resources** (search *Azure AI services* → **Manage deleted resources**) → select it → **Purge**.

Your GitHub repo can stay: it costs nothing and shows your work.

## Optional: publish the fine-tuning lab with GitHub Pages

1. Your repo on GitHub → **Settings** → **Pages**.
2. **Source:** *Deploy from a branch*. **Branch:** `main`, folder **/ (root)** → **Save**.
3. After 1–2 minutes: `https://<your-username>.github.io/nakoba-genaiops-mlops-labs/genaiops/finetuning-lab/`

[⬅ Fine-tuning](04-fine-tuning.md) | [🏠 Track home](../README.md) | [Next: Troubleshooting ➡](06-troubleshooting.md)
