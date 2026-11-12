# Scoring rubric (8 dimensions, 1–5 each, total /40)

Score with the anchors below, not by feel. When an idea falls between two anchors, pick the lower one unless a receipt justifies the higher. Every score needs a one-line reason that cites a receipt, graveyard finding or critic point.

Higher is always better. Dimension 4 is phrased as *ease*, so 5 = fast to build.

| # | Key | Dimension | 1 | 3 | 5 |
|---|---|---|---|---|---|
| 1 | `pain` | Pain Severity | Nice-to-have; few complaints, no workaround effort | Recurring annoyance; people tolerate a clunky workaround | Daily money/time bleed; people pay for or build painful workarounds, quantified cost |
| 2 | `economics` | Business Viability & Unit Economics | No clear payer, or margins destroyed by ops/logistics (graveyard trap) | Someone would pay, but price sensitivity or ops cost is unclear | Clear budget owner, price ≥ evidence of current spend, software-like margins |
| 3 | `distribution` | Distribution & GTM Ease | Only reachable through paid ads or long enterprise sales with no wedge | Reachable via outbound/communities with effort | Buyers cluster in known communities/channels; organic or founder-led sales is credible |
| 4 | `build_ease` | Build Ease | Heavy R&D, hardware, licences, or 12+ months to MVP | 1–3 months to a usable MVP | MVP in 1–3 weeks with existing APIs/LLMs |
| 5 | `moat` | Competitive Moat / Wedge | Commodity; incumbents can ship it as a feature tomorrow | Wedge exists (niche, workflow, geography) but copyable in a year | Compounding advantage: data, network effects, integrations, regulatory position |
| 6 | `evidence` | Evidence Strength | Mostly inferred; verification failed | Receipts from 2 source types, some snippet-only | 3+ source types, verified receipts, curated backing (YC RFS / Fix My Itch) |
| 7 | `why_now` | Historical Fixability / Why Now | Graveyard tarpit with unchanged structural flaw | Partial fix, or no precedent and no specific "why now" | Specific new shift directly removes the cause of past deaths, or a clean blue-ocean wedge with a dated trigger |
| 8 | `fmf` | Founder–Market Fit | No relevant skill, network or access; would be learning the market from zero | Some adjacent experience or access to buyers | Direct domain experience, existing distribution, or a skill that is the hard part |

Score 2 and 4 sit between the anchors.

**Evidence caps:** if the verifier flagged an idea's evidence as unreliable (>1/3 failed), `evidence` ≤ 2. If all receipts are snippet-only, `evidence` ≤ 3.
**FMF unscored:** if the user gave no background, set `fmf` to 3 and `"fmf_unscored": true`.

## Verdicts (applied by `scripts/score.py`)

- 🟢 **Strong Build**: 32–40, and no dimension at 1, and `evidence` ≥ 3
- 🟡 **Conditional**: 24–31, or ≥32 but blocked by a gate. Name the lowest-scoring risk to test first
- 🔴 **Tarpit / Pass**: below 24, or `why_now` = 1 (unchanged graveyard flaw)

## scores.json format

```json
{
  "mode": "full",
  "ideas": [
    {
      "name": "GST reconciliation copilot",
      "scores": {"pain": 5, "economics": 4, "distribution": 3, "build_ease": 4,
                 "moat": 2, "evidence": 4, "why_now": 4, "fmf": 3},
      "reasons": {"pain": "…", "economics": "…", "distribution": "…", "build_ease": "…",
                  "moat": "…", "evidence": "…", "why_now": "…", "fmf": "…"},
      "fmf_unscored": false
    }
  ]
}
```
