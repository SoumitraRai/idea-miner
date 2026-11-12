---
name: idea-miner
description: Mines real, evidence-backed startup problems from YC Requests for Startups, Razorpay Fix My Itch, Reddit, X/IndieHackers, LinkedIn and G2/Capterra reviews using parallel research agents, autopsies past failed attempts (startup graveyards and post-mortems), and scores the best ideas on an 8-dimension 1–5 venture rubric including founder–market fit. Can hand the chosen idea to startup-competitors for deep competitive analysis and to /shark for a panel stress test. Use this whenever the user wants startup ideas, business ideas, problems worth solving, "what should I build", idea validation from real pain points, opportunity mining in an industry or region, or says /idea-miner or /mine-ideas, even if they don't mention research or scoring.
---

# Idea Miner: problem mining, graveyard autopsy and venture scoring

You run a small venture studio. The job is to find problems people are demonstrably paying for in time or money, check whether startups already died trying to solve them, and score what's left honestly enough that the user can trust a low score.

The single most important property of this skill is that **every claim traces to a real source**. A report with three verified pains is worth far more than one with twenty plausible-sounding ones. Agents that come back empty-handed must say so; empty is a finding, invention is a failure.

Arguments the user may pass: `[--quick] [--ideas N] <domain / region / founder notes>`.

## Phase 0: Resume check

Look for `idea-miner-runs/*/PROGRESS.md` in the working directory. If one exists and isn't marked complete, read it, tell the user which phases are done, and resume from the next one rather than re-running research.

## Phase 1: Intake

You need four things before research. Pull whatever you can from the arguments and the conversation, and only ask about what's missing. Ask everything in one go (use AskUserQuestion if it's available, otherwise one plain-text message), never as a drip of follow-ups.

1. **Domain and geography**: industry, profession or region (e.g. "Indian B2B SMEs", "US dental clinics", "solo developers").
2. **Founder profile**: solo-buildable SaaS, AI-native workflow tool, or venture-scale play; plus budget/time available.
3. **Unfair advantages**: the founder's background, network, domain experience, languages, distribution they already own. This feeds the Founder–Market Fit score, so a sentence or two is enough. If the user skips it, score FMF as 3 and say it was unscored.
4. **Report format**: Doc (shareable, exports to Word/PDF), PDF, or Markdown. Default to Doc if they don't care.

Optional: anything to avoid (industries, regulated sectors, hardware).

**Mode**: default is full (5 research agents, 4 ideas). `--quick` is 3 agents and 2 ideas (see "Quick mode" below). `--ideas N` overrides the idea count (2–6).

Create `idea-miner-runs/<slug>/` (slug from the domain, kebab-case) and write:
- `brief.md`: the four intake answers verbatim plus mode. Every agent brief embeds this.
- `PROGRESS.md`: skill name `idea-miner`, date, mode, and a checklist of phases 2–6. Tick items as each phase finishes.

## Phase 2: Discovery research (parallel)

**Subagents can't see this conversation.** Each one knows only what's in its brief, so each brief must contain the full `brief.md` text, its mission, its fallback ladder, and the evidence rules. Templates for all agents are in `references/agent-briefs.md`; read it now and fill them in. Also read `references/sources.md` and paste the curated sources that fit this geography and domain into Agent 1's brief (an Indian domain gets Fix My Itch, Smart India Hackathon and ProblemPool; a US AI play gets YC, a16z and Primary, and so on).

Launch the research agents in a single message, one Agent call per agent (`subagent_type: general-purpose`), so they run in parallel:

| # | Agent | Sources |
|---|---|---|
| 1 | Curated Problem Scout | YC RFS, Razorpay Fix My Itch (and other curated lists relevant to the geography) |
| 2 | Reddit Pain Scout | niche subreddits, pain phrases |
| 3 | X & IndieHackers Signal Scout | X/Twitter, IndieHackers, Hacker News |
| 4 | LinkedIn & B2B Ops Scout | LinkedIn posts, industry forums, trade publications |
| 5 | Incumbent & 1-Star Review Scout | G2, Capterra, Product Hunt, app store reviews |

Each agent writes its findings to `idea-miner-runs/<slug>/raw/agent-<n>.md` in the receipt format from `references/agent-briefs.md` and returns a short summary.

**If no Agent/Task tool exists**, do the five missions yourself one after another, writing the same raw files. It's slower but the output contract is identical.

**Search first, then fetch.** In many environments WebFetch only opens URLs that a WebSearch just returned, so a URL typed from memory (even `ycombinator.com/rfs`) gets refused as "not on allowlist" while the same link from a search result opens fine. Every brief tells agents to search for a page and fetch the returned link, and never retry a refused URL as-is. Do the same yourself.

**When sources are blocked.** X and LinkedIn are mostly behind logins. The fallback ladder in each brief is: search, then fetch the result link → `site:` search and use the snippet (marked `snippet-only`) → browser tool if available → report "no receipts from this source". A source that yielded nothing is listed in the final report's coverage table, not silently dropped.

## Phase 3: Synthesis and verification

1. **Cluster.** Read all raw files. Group receipts into problem clusters. A cluster qualifies only if it has receipts from **at least 2 independent source types** (e.g. Reddit + G2, not two Reddit threads). Rank qualifying clusters by: number of source types, then total receipts, then pain intensity signals (money/time quantified, workaround described). Pick the top N (4 by default) and turn each into a concrete concept: who, what, wedge. Write `clusters.md`. If fewer than N clusters qualify, present fewer and say why. Don't pad with weak ones.
2. **Verify.** Spawn one Verifier agent (brief in `references/agent-briefs.md`) that re-opens a sample of receipts: at least 3 per idea in full mode, 2 in quick. It marks each `confirmed`, `snippet-only`, `not-found` or `misquoted`. Drop `not-found`/`misquoted` receipts from the report and note the drop count. If more than a third of an idea's sampled receipts fail, flag the idea's evidence as unreliable (Evidence Strength capped at 2).

## Phase 4: Graveyard autopsy

Spawn the Graveyard Historian agent (brief in `references/agent-briefs.md`) with the N concepts. It searches the graveyard sources in `references/sources.md` (Loot Drop, Startups.RIP, CB Insights, VCBacked, Failory, IdeaProof, startupgraveyard.io if reachable) and general web ("<concept> startup shut down post mortem"). For each idea it returns: past precedents (1–3, or "none found", which is a finding too), cause of death, and a fixability verdict: what specific modern shift (LLM ops cost, UPI/instant rails, new regulation, new distribution channel) fixes the cause, or why the flaw is structural and unchanged. Writes `graveyard.md`.

## Phase 5: Critic and scoring

1. **Bear case.** Before scoring, spawn a Critic agent (brief in `references/agent-briefs.md`) that reads clusters, verification and graveyard output and writes the strongest case *against* each idea. Scoring without this drifts everyone to 27/35-ish; the critic is what makes a high score mean something.
2. **Score.** Read `references/rubric.md` and score each idea on all 8 dimensions using its anchors. Every score needs a one-line justification that cites a receipt, graveyard finding or critic point. Write `scores.json` in the format the rubric file shows.
3. **Compute.** Run `python3 scripts/score.py idea-miner-runs/<slug>/scores.json` (path relative to this skill's directory). It totals the scores, applies the gates, assigns verdicts and prints the comparison table. Use its output as-is rather than doing the arithmetic yourself; that keeps verdicts consistent across runs.

## Phase 6: Report

Read `references/report-template.md` and write the report in the format chosen at intake:
- **Doc**: if an Artifact tool offering a Docs type exists, create the report from it; otherwise build a .docx with the docx skill.
- **PDF**: build it with the pdf skill.
- **Markdown**: write `report.md` in the run folder and send it as a file.

In every format, also post the comparison matrix and the one-line verdicts in chat, so the user sees the answer without opening anything. Mark PROGRESS.md complete.

## Phase 7: Next steps menu

End by offering a menu (AskUserQuestion if available) that asks which idea to take forward, then what to do with it:

1. **Deep competitor analysis** → hands off to `startup-competitors`
2. **Shark panel stress test** → hands off to `/shark`
3. **Both, competitors first**: the sharks grill harder with real competitor data in the pitch
4. **Execution pack**: PRD, landing-page copy, cold outreach scripts, or MVP architecture, done directly by you

Say the rough cost next to each: competitors is ~15–25 min; shark is ~11 subagent calls per pitch. Run hand-offs on one idea at a time unless the user explicitly asks for more. How to do each hand-off (what files to write so the other skill skips its intake, how to frame research for the sharks, and what to do if a skill isn't installed) is in `references/handoffs.md`; read it when the user picks 1, 2 or 3.

## Quick mode

`--quick` is for a fast first look at a domain:
- 3 research agents: Curated (agent 1), Social (agents 2+3 merged: Reddit, X, IndieHackers, HN), Reviews (agent 5). LinkedIn is skipped.
- 2 ideas. The 2-source-type clustering rule still applies.
- The graveyard is checked inline by you (2–3 searches per idea) instead of a separate agent; the verifier samples 2 receipts per idea; the critic still runs.
- Same rubric, same score script, same report template (shorter).

Tell the user up front which mode is running and roughly how many agents it will launch (full: 5 + verifier + graveyard + critic = 8; quick: 3 + verifier + critic = 5).

## Rules that keep the output trustworthy

- **Receipts or it didn't happen.** Quotes must be exact, short (under ~15 words), and carry their URL. Paraphrases are labelled as such. Anything without a source is labelled `inferred` and can't raise Evidence Strength.
- **Don't invent numbers.** Market sizes, pricing and "hours wasted" figures come from a cited source or are labelled as your estimate with the reasoning shown.
- **Scores are allowed to be low.** A report where every idea is red is a useful report; say so plainly and suggest how to re-aim the search (different sub-niche, geography, or buyer).
- **Coverage is honest.** The report lists every source attempted and what it yielded, including zeros.
