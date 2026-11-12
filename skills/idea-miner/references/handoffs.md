# Hand-offs to other skills

Both target skills are invoked through the Skill tool by whatever name appears in the session's skill list (e.g. `startup-competitors` or `anthropic-skills:startup-competitors`; `shark` or `anthropic-skills:shark`). Check the list first. If a skill isn't there, use the fallback described below and tell the user in one line which skill would do it better if installed.

Run one idea at a time. Before launching, confirm the cost in one line (it's already in the menu, so don't re-ask if the user just chose it).

---

## 1. startup-competitors

That skill skips its intake interview when it finds startup-design style files, and it resumes from a `PROGRESS.md` that names it. Use that: pre-write its inputs so it goes straight to research.

Create `idea-miner-runs/<slug>/handoff-<idea-slug>/` and write:

- `00-intake/brief.md`: product one-liner, problem, target buyer, geography, pricing hypothesis, the differentiator/wedge, and the founder profile from `brief.md`.
- `01-discovery/competitor-landscape.md`: every incumbent agent 5 found (name, URL, pricing, top complaints with links) plus any competitors mentioned in other raw files. Mark this as a surface-level starting list.
- `01-discovery/target-audience.md`: the pain receipts for this idea (quotes + links) and who has them.
- `01-discovery/market-analysis.md`: graveyard findings and any market/regulatory facts gathered, with sources.

Don't create a `PROGRESS.md` there. The competitor skill makes its own.

Then `cd` into that hand-off folder (or tell the skill it's the project directory) and invoke the Skill with args like:
`Deep competitive analysis for "<idea>". Prior discovery files are in <path>; use them and skip intake. Geography: <geo>.`

It will still ask the user to choose a research depth (light / standard / deep). That's its own checkpoint, so let it ask.

When it finishes, add a short "Competitive update" to the idea-miner report: did the deep dive change the `moat` or `distribution` score? If so, update `scores.json`, re-run `score.py`, and show the before/after.

**Fallback (skill not installed):** do a lighter version yourself: 3–5 incumbents with pricing, top review complaints, and a one-paragraph wedge statement.

---

## 2. /shark

The shark panel's subagents only know what's in the pitch file, and the shark skill deliberately refuses to add numbers or traction the founder never gave. That's good. It means the panel grills the real gaps. So don't dress research up as traction. Give it the idea plus clearly labelled research context, and let the sharks attack the unknowns.

Before invoking, post a short **pitch context** message in the conversation (the shark skill builds its pitch file from the conversation):

```
Pitch context for the shark panel: <idea name>
- Idea (one sentence): …
- Who it's for / who pays: …
- Founder: <from brief.md: background, time, budget>
- What research found (not traction, third-party evidence):
  - Pain receipts: <3–5 short quotes with links>
  - Incumbents & pricing: <names, prices>
  - Past failures: <precedents + cause of death + why-now claim>
- What we do NOT know yet: customers, price tested, CAC, retention
- Planned 72-hour test: …
```

If a competitor deep-dive ran first, add its key battle-card points under "Incumbents".

Then invoke the shark Skill with the idea as args, e.g. `"<idea one-liner>"` (add `--investors 3` if the user wants it cheaper). Let the shark skill run its own flow, including its own pitch file and its own cost line. Don't write questions, answers or decisions for it.

Afterwards, add one line to the idea-miner report linking the shark BOARD.md and noting whether the panel's top objection matches the critic's. Don't change scores based on shark offers; they're practice numbers, not evidence.

**Fallback (skill not installed):** run a short three-voice panel yourself (Numbers, Skeptic, Customer), each giving its hardest question and an IN/OUT, clearly labelled as a lightweight stand-in.

---

## 3. Both

Run startup-competitors first, update scores, then shark with the enriched pitch context. Tell the user both costs together before starting.
