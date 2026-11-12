# Idea Miner

A Claude plugin that finds startup ideas from **real, linked evidence** rather than brainstorming. It sends parallel research agents to mine pain points, checks whether startups already died trying, has a critic argue against each idea, and then scores the survivors on an 8-dimension venture rubric. Every quote in the report links back to its source.

## What it does

1. **Intake** asks four questions in one go: your domain and geography, founder profile, unfair advantages, and report format (Doc, PDF or Markdown).
2. **Discovery** sends five agents out in parallel:
   - curated lists (YC Requests for Startups, Razorpay Fix My Itch, VC wish-lists)
   - Reddit
   - X, IndieHackers and Hacker News
   - LinkedIn and B2B forums
   - G2, Capterra and app-store 1-star reviews
3. **Synthesis** clusters the findings. A problem only counts if it appears in at least two different kinds of source.
4. **Verification** has an agent reopen a sample of the quotes and drop any that can't be found.
5. **Graveyard autopsy** looks for past attempts on Loot Drop, Startups.RIP, CB Insights, VCBacked and Failory: who tried, why they died, and whether anything has changed since.
6. **Critic** writes the strongest case against each idea before it's scored.
7. **Scoring** rates each idea from 1 to 5 on Pain, Economics, Distribution, Build Ease, Moat, Evidence, Why Now and Founder–Market Fit, for a total out of 40. The bundled `score.py` adds up the totals and applies the gates, so verdicts stay consistent:
   - 🟢 Strong Build: 32–40, with no dimension at 1 and evidence of at least 3
   - 🟡 Conditional: 24–31, or 32+ but blocked by a gate
   - 🔴 Tarpit / Pass: below 24, or a past failure whose cause is still unfixed
8. **Report and next steps** gives a comparison matrix, receipts, autopsies and a 72-hour validation test for each idea. It then offers a menu:
   - a deep competitor analysis
   - a Shark Tank-style stress test
   - both, competitors first
   - an execution pack (PRD, landing-page copy, outreach scripts, MVP architecture)

`--quick` runs 3 agents and keeps 2 ideas, for a fast first look at a new domain.

## Install

**Claude Code:**

```
/plugin marketplace add SoumitraRai/idea-miner
/plugin install idea-miner@idea-miner
```

**Claude.ai or the desktop app:** download the repo as a zip (or use a release `.plugin` file) and upload it from the plugins/skills settings.

**Just the skill:** copy `skills/idea-miner/` into `~/.claude/skills/`.

## Usage

```
/idea-miner Indian B2B SMEs, solo-buildable AI SaaS. I'm a backend dev with 3 years in fintech.
/idea-miner US dental clinics --quick
/idea-miner Shopify store owners in India --ideas 3
```

Or just ask: *"what startup should I build for Indian logistics SMEs?"*

Runs save to `idea-miner-runs/<domain>/` with a progress file, so an interrupted run picks up where it stopped.

## Optional companion skills

Idea Miner works on its own. If these skills are installed, it hands off to them from the next-steps menu:

| Skill | What it adds | Without it |
|---|---|---|
| `startup-competitors` | Battle cards, pricing landscape, feature matrix. Idea Miner pre-writes its input files so it skips its own questions. | Idea Miner does a lighter competitor scan itself |
| `shark` | A Shark Tank-style panel that grills the idea and decides IN or OUT. | Idea Miner runs a short three-voice panel |

## Notes and limits

- **Search first, then fetch.** Some environments only let Claude open a page whose link came from a search result. A typed URL, even `ycombinator.com/rfs`, can be refused. The agents are told to search for a page and then open the link the search returned, which works around this.
- **X and LinkedIn** are mostly behind logins, so their evidence is usually marked `snippet-only`, meaning only a search-result snippet was seen. The report lists every source tried and what it returned, including zeros.
- **Scores are allowed to be low.** A report where everything comes out red is a useful result.
- **Cost.** A full run launches about 8 agents, and quick mode about 5.

## Structure

```
.claude-plugin/
  plugin.json          plugin manifest
  marketplace.json     lets people install from this repo
skills/idea-miner/
  SKILL.md             the workflow
  references/          agent briefs, rubric, sources, report template, hand-offs
  scripts/score.py     totals, gates and verdicts
```

## License

MIT
