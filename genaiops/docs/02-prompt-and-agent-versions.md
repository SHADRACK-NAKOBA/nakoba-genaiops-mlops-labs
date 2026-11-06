# GenAIOps Lab 2 – Develop prompt and agent versions

[⬅ Setup](01-setup-foundry.md) | [🏠 Track home](../README.md) | [Next: Design and optimize prompts ➡](03-design-optimize-prompts.md)

**Scenario.** You're building the **Trail Guide Agent** for Adventure Works (a fictional outdoor company). Version 1 gives basic hiking advice; users want personalised, structured, safer guidance. Instead of rebuilding the app, you **improve the system prompt** and deploy **three versions** of the same agent, marking each release with a **Git tag**.

**Time:** about 30 minutes. **Cost:** a few cents of model usage.

| Concept | In this lab |
|---|---|
| **Prompt engineering** | The instructions in `prompts/v1…v3_instructions.txt` decide how the agent behaves |
| **Agent versioning** | Each run of the script creates a new **version** of the agent `trail-guide` (1, 2, 3) |
| **Foundry Agent Service** | Hosts the agent and its versions; you test them in the portal |
| **Git tags** | `v1`, `v2`, `v3` mark which commit produced which agent version |

> Before you start: finish [setup](01-setup-foundry.md). In VS Code's terminal you're in the **genaiops** folder with **(.venv)** active.

---

## 2.1 Look at the three prompts

In VS Code's Explorer open **genaiops → src → agents → trail_guide_agent → prompts** and read:

| File | What it adds |
|---|---|
| `v1_instructions.txt` | Basic trail-guide role |
| `v2_instructions.txt` | **Personalisation**: asks about experience, fitness and preferences |
| `v3_instructions.txt` | **Production-ready**: structured answers, safety, weather, step-by-step planning |

## 2.2 Deploy version 1

1. Open **src/agents/trail_guide_agent/trail_guide_agent.py**. Find this line and check it reads **v1**:
   ```python
   prompt_file = Path(__file__).parent / 'prompts' / 'v1_instructions.txt'
   ```
2. In the terminal:
   ```bash
   python src/agents/trail_guide_agent/trail_guide_agent.py
   ```
   Expected:
   ```
   Agent created (id: trail-guide:1, name: trail-guide, version: 1)
     prompt: v1_instructions.txt   model: gpt-5.1
   ```
   > ❌ *PermissionDenied* right after `azd up`? Role assignments take up to 10 minutes. Wait and run again ([T6](06-troubleshooting.md#t6-permissiondenied-or-401-when-running-a-script)).
3. Commit and tag this release:
   ```bash
   git add src/agents/trail_guide_agent/trail_guide_agent.py
   git commit --allow-empty -m "Deploy trail guide agent V1"
   git tag v1
   ```
   > `--allow-empty` lets you commit even though V1 needed no code change: the tag still marks the release point.

## 2.3 Test version 1 in the Foundry portal

1. Open https://ai.azure.com and sign in.
2. If you see a **New Foundry** toggle at the top, switch it **on**.
3. Select your project **ai-project-<env-name>** (top-left project picker, or **View all projects**).
4. Click **Build** in the top bar → **Agents** in the left menu → click **trail-guide**.
5. The **playground** opens. The latest version (**1**) is selected. (You can switch versions with the version picker at the top of the agent page, or on its **Versions** tab.)
6. Ask:
   - `What gear do I need for a day hike?`
   - `Recommend a trail near Seattle for beginners`

Note how general the answers are. That's your baseline.

## 2.4 Deploy version 2 (personalisation)

1. In **trail_guide_agent.py** change `v1_instructions.txt` to **`v2_instructions.txt`** and **save** (Ctrl+S):
   ```python
   prompt_file = Path(__file__).parent / 'prompts' / 'v2_instructions.txt'
   ```
2. Run it:
   ```bash
   python src/agents/trail_guide_agent/trail_guide_agent.py
   ```
   Expected: `... version: 2` and `prompt: v2_instructions.txt`.
3. Commit and tag:
   ```bash
   git add src/agents/trail_guide_agent/trail_guide_agent.py
   git commit -m "Deploy trail guide agent V2 with enhanced capabilities"
   git tag v2
   ```

## 2.5 Deploy version 3 (production-ready)

1. Change `v2_instructions.txt` to **`v3_instructions.txt`** and save.
2. Run:
   ```bash
   python src/agents/trail_guide_agent/trail_guide_agent.py
   ```
   Expected: `... version: 3` and `prompt: v3_instructions.txt`.
3. Commit and tag:
   ```bash
   git add src/agents/trail_guide_agent/trail_guide_agent.py
   git commit -m "Deploy trail guide agent V3 with production features"
   git tag v3
   ```

## 2.6 Compare the versions

### Version history in Git
```bash
git tag
git log --oneline --decorate -5
```
You'll see `v1`, `v2`, `v3`, each on its own commit. To see exactly what changed between releases:
```bash
git diff v2 v3 -- src/agents/trail_guide_agent/trail_guide_agent.py
```

### Prompt differences
In VS Code, right-click `v1_instructions.txt` → **Select for Compare**, then right-click `v2_instructions.txt` → **Compare with Selected**. Do the same for v2 → v3.

- **V1 → V2:** personalisation and fuller guidance
- **V2 → V3:** a structured framework, safety and planning steps

### Behaviour in the portal
In the playground, use the **version picker** to switch between versions 1, 2 and 3, and ask each one the **same** question:

> `I'm planning a weekend hiking trip near Seattle. What should I know?`

| Version | What you should notice |
|---|---|
| 1 | Basic trail ideas and general advice |
| 2 | Asks about your experience and preferences, tailors the advice |
| 3 | Structured plan: safety, weather, permits, gear, step-by-step |

## 2.7 Save your work to GitHub

```bash
git push origin main --tags
```

## ✅ Check

- [ ] Agent **trail-guide** has versions 1, 2 and 3 in the portal
- [ ] `git tag` shows `v1 v2 v3`
- [ ] You can explain what each prompt version added

> Leave the script on **v3**: Lab 3 starts from it.

[⬅ Setup](01-setup-foundry.md) | [🏠 Track home](../README.md) | [Next: Design and optimize prompts ➡](03-design-optimize-prompts.md)
