# GenAIOps – Interview questions from these labs

[🏠 Track home](../README.md)

**60-second pitch:** "I ran a GenAIOps workflow for an AI trail-guide agent on Microsoft Foundry. Infrastructure is code: `azd up` deploys the Foundry project and two models. I versioned the agent's system prompt through three releases, tagging each in Git so every agent version maps to a commit. Then I treated prompt changes like experiments: measured a baseline on five fixed test prompts, tested a concise prompt and a smaller model on separate branches, scored quality on intent, relevance and groundedness, compared token usage, and merged the cheapest option that kept quality. Finally I practised choosing between SFT, DPO and RFT from evaluation metrics, and curating valid training data for each."

| Question | Strong answer |
|---|---|
| Why version prompts in Git? | Prompts are code: they change behaviour. Versioning gives history, review, diff, rollback, and a link between an agent version and the commit that produced it. |
| Why a baseline first? | Without it you can't prove an improvement, or notice a regression. It's the quality floor and the token/cost benchmark. |
| Why experiment branches? | They isolate changes from production. Each branch changes one variable (prompt *or* model), so the result is attributable. You merge only the winner. |
| How did you measure quality? | The same 5 test prompts every run, scored 1–5 on intent resolution, relevance and groundedness. In production I'd automate it with Foundry evaluators or an LLM-as-judge and a bigger test set. |
| Prompt optimization vs a smaller model: which first? | Usually the prompt: it's cheap to try and keeps model quality. A smaller model cuts per-token cost further but may lose depth. The data decides; small models suit simple, high-volume queries. |
| What is token cost made of? | Input tokens (system prompt + conversation) plus output tokens. A concise prompt reduces both: a shorter system prompt and shorter answers. |
| When fine-tune instead of prompt? | When a consistent behaviour can't be achieved with prompts and RAG: a strict format at scale, tone calibration, or complex reasoning. It costs more and needs good data, so try prompts first. |
| SFT vs DPO vs RFT? | SFT teaches format/style from complete ideal answers. DPO teaches preferences from chosen vs rejected pairs. RFT teaches reasoning with a grader that scores objective criteria. |
| What makes training data invalid? | Wrong format for the method, missing responses, mislabeled or flipped pairs, examples from another task, and subjective or proxy graders (like word count). |
| Why `azd` / Bicep? | Repeatable, reviewable environments. Everyone gets the same resources, and `azd down --purge` removes them completely. |
| What went wrong, and how did you fix it? | Example: the tutorial's gpt-4.1 can't be deployed by new subscriptions any more (deprecated). I switched to the GA gpt-5.1 and gpt-5-mini and deployed both from the Bicep template. |

[🏠 Track home](../README.md)
