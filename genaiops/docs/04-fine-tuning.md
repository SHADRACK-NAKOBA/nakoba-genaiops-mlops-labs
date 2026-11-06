# GenAIOps Lab 4 – Optimize AI agents with fine-tuning

[⬅ Design and optimize prompts](03-design-optimize-prompts.md) | [🏠 Track home](../README.md) | [Next: Share and clean up ➡](05-share-and-cleanup.md)

**Scenario.** You're an AI engineer at Adventure Works. The Trail Guide Agent has **three quality problems** that better prompts didn't fix. For each one you read the evaluation metrics, find the root cause, choose the right fine-tuning method, and pick **exactly the 3 valid training examples** from a mixed dataset.

**Time:** about 20 minutes. **Cost: free.** It's an interactive simulation in your browser: no Azure resources, no fine-tuning bill.

| Method | Fixes | Training data looks like |
|---|---|---|
| **SFT** (Supervised Fine-Tuning) | Inconsistent **format/style** | Prompt + the complete ideal response ("labeled example") |
| **DPO** (Direct Preference Optimization) | Wrong **tone** or preferences | Prompt + a **preferred** and a **rejected** response ("preference pair") |
| **RFT** (Reinforcement Fine-Tuning) | Weak **multi-constraint reasoning** | Prompt + a **grader** with objective, measurable scoring criteria |

**Evaluation metrics** (coherence, fluency, relevance, groundedness, tool-call accuracy, safety) tell you *which kind* of problem you have, and that decides the method. Wrong method or wrong data = wasted time and money, or a worse model.

---

## 4.1 Open the interactive lab

The lab is in this repo, so no internet sign-in is needed.

1. In VS Code's Explorer, open **genaiops → finetuning-lab**.
2. Right-click **index.html** → **Reveal in File Explorer** (Mac: **Reveal in Finder**).
3. **Double-click** `index.html`. It opens in your browser.

> Prefer a link? If the repo owner turned on GitHub Pages, it's at `https://<owner>.github.io/<repo>/genaiops/finetuning-lab/` ([how](05-share-and-cleanup.md#optional-publish-the-fine-tuning-lab-with-github-pages)).

You'll see three scenario cards. Do them in any order.

## 4.2 Scenario 1 – Inconsistent response format → SFT

1. Click **Explore this scenario →** on the blue **Scenario 1** card. Read the metrics: similar gear questions get answers with different levels of detail.
2. Look at all **9** cards. The valid ones are **Labeled Examples** with a complete Adventure Works response: product name, specs, price, stock by location, and complementary items.
3. Click these **3** cards:
   - ✅ *"What's the best 3-season tent for solo backpacking under $400?"* (full spec, price, stock by location, complements)
   - ✅ *"Compare Merrell Moab 3 vs Salomon X Ultra 4 for rocky trails."* (structured side-by-side with a recommendation)
   - ✅ *"What gear do I need for a full-day summer hike in Rocky Mountain National Park?"* (multi-item list with specs, price, stock)
4. **Don't** select these, and know why:
   | Card | Why it's invalid for SFT |
   |---|---|
   | "Best rain jacket for hiking?" | Vague, promotional, no structure |
   | "What trekking poles would you recommend?" | Incomplete: no response recorded |
   | "Is the Cascade Mountain safe for beginners?" | A preference pair (DPO data) |
   | "Plan a 3-day hiking trip…" | Prompt + grader (RFT data) |
   | "Trail difficulty rating for the Maroon Bells loop?" | Not a gear-specification example |
   | "Tell me about the MSR Hubba Hubba NX tent." | Missing price, stock and complements |
5. The counter shows **3 of 3 examples selected** → click **Submit selection**. You should see **Score: 3/3 correct**.
6. Click **⚙ Generate JSONL**. The training file appears **on the page** (it isn't downloaded): one JSON object per line, each with a `user` and an `assistant` message. To keep it, copy the text into a new file called `sft_training_data.jsonl`.
7. Click **📓 Run the SFT Notebook →**. Read the walkthrough: upload data → set hyperparameters → submit the fine-tuning job → deploy → evaluate. It's a simulation, so nothing runs in Azure.

## 4.3 Scenario 2 – Inappropriate tone on sensitive topics → DPO

1. Go back to the scenario page → **Explore this scenario →** on the green **Scenario 2** card.
2. For each preference pair, ask: is the **preferred** answer balanced, practical and encouraging? Is the **rejected** one an extreme (alarmist *or* dismissive)?
3. Select these **3**:
   - ✅ *"I've never rock climbed before. Can I attempt the via ferrata on my first trip?"* (balanced vs alarmist)
   - ✅ *"My kids are 8 and 10. Is winter camping safe for them?"* (actionable vs fear-based)
   - ✅ *"I'm a moderate hiker. Is the Knife's Edge trail suitable for me?"* (encouraging vs dismissive)
4. **Don't** select:
   | Card | Why |
   |---|---|
   | Sleeping bag temperature rating | Both answers fine: no tone contrast to learn from |
   | Crampons for glacier hiking | A labeled example (SFT data) |
   | Heart condition at altitude | **Bad label**: the "preferred" answer ("just take it easy!") is dangerously dismissive |
   | Summit with afternoon thunderstorms | **Flipped labels**: the "rejected" answer is actually safer |
   | MSR Hubba NX vs Big Agnes weight | Gear comparison, not a tone problem |
   | Plan a 3-day high-altitude trip | Prompt + grader (RFT data) |
5. **Submit selection** → **Score: 3/3 correct** → **⚙ Generate JSONL** (each line has `prompt`, `chosen` and `rejected`) → **📓 Run the DPO Notebook →**.

## 4.4 Scenario 3 – Illogical reasoning in complex planning → RFT

1. **Explore this scenario →** on the pink **Scenario 3** card.
2. A card is valid only if **both** are true: the prompt has **several constraints that interact**, and the grader's criteria are **specific, objective and measurable**.
3. Select these **3**:
   - ✅ *"Plan a 4-day backpacking loop for two people: one experienced, one first-time… $150… late October in the San Juan Mountains."*
   - ✅ *"My group: one runner (high fitness), one returning from injury (low fitness), one child aged 12…"*
   - ✅ *"I want to summit a 14er… Solo trip, $500 gear budget… one weekend from Denver… early June."*
4. **Don't** select:
   | Card | Why |
   |---|---|
   | Elevation of Longs Peak | Single fact lookup: no reasoning to train |
   | Week-long family trip in Glacier NP | Incomplete: no grader recorded |
   | Waterproof jacket for the Pacific Northwest | A labeled example (SFT data) |
   | Hiking alone in bear country | A preference pair (DPO data) |
   | "Score 1 if the plan looks good" | Subjective grader, can't be measured |
   | "Score 1 if longer than 100 words" | Rewards padding, not correct reasoning |
5. **Submit selection** → **Score: 3/3 correct** → **⚙ Generate JSONL** (each line has a `prompt` and its `grader_criteria`) → **📓 Run the RFT Notebook →**.

## Key takeaways

- **Diagnose first.** Metrics tell you whether it's a format, tone or reasoning problem.
- **Each method needs its own data format.** SFT data can't train DPO, and so on.
- **Bad data hurts.** Incomplete, mislabeled or flipped examples make the model worse.
- **Try prompts first** (Labs 2–3): fine-tuning costs more and takes longer.

## ✅ Check

- [ ] All three scenarios scored 3/3
- [ ] You can explain when to use SFT, DPO and RFT, and what data each needs

[⬅ Design and optimize prompts](03-design-optimize-prompts.md) | [🏠 Track home](../README.md) | [Next: Share and clean up ➡](05-share-and-cleanup.md)
