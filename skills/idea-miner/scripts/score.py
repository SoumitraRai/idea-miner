#!/usr/bin/env python3
"""Total idea-miner scores, apply gates, assign verdicts, print a markdown matrix.

Usage: python3 score.py path/to/scores.json
Writes the computed fields back into scores.json (total, verdict, gate_notes)
and prints the comparison table to stdout.
"""
import json
import sys

DIMS = [
    ("pain", "Pain"),
    ("economics", "Economics"),
    ("distribution", "Distribution"),
    ("build_ease", "Build Ease"),
    ("moat", "Moat"),
    ("evidence", "Evidence"),
    ("why_now", "Why Now"),
    ("fmf", "Founder Fit"),
]
GREEN, YELLOW, RED = "🟢 Strong Build", "🟡 Conditional", "🔴 Tarpit / Pass"


def verdict(scores):
    total = sum(scores[k] for k, _ in DIMS)
    notes = []
    if scores["why_now"] == 1:
        notes.append("Why Now = 1: unchanged graveyard flaw")
        return total, RED, notes
    if total < 24:
        return total, RED, notes
    if total >= 32:
        ones = [label for k, label in DIMS if scores[k] == 1]
        if ones:
            notes.append("gate: dimension at 1 (" + ", ".join(ones) + ")")
        if scores["evidence"] < 3:
            notes.append("gate: evidence below 3")
        return total, (YELLOW if notes else GREEN), notes
    return total, YELLOW, notes


def main(path):
    with open(path) as f:
        data = json.load(f)
    errors = []
    for idea in data["ideas"]:
        s = idea.get("scores", {})
        for k, _ in DIMS:
            v = s.get(k)
            if not isinstance(v, int) or not 1 <= v <= 5:
                errors.append(f"{idea.get('name', '?')}: '{k}' must be an integer 1-5, got {v!r}")
    if errors:
        sys.exit("score.py: invalid scores\n  " + "\n  ".join(errors))

    for idea in data["ideas"]:
        total, v, notes = verdict(idea["scores"])
        weakest = min(DIMS, key=lambda d: idea["scores"][d[0]])
        idea.update(total=total, verdict=v, gate_notes=notes, weakest=weakest[1])
    data["ideas"].sort(key=lambda i: i["total"], reverse=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    head = "| Idea | " + " | ".join(l for _, l in DIMS) + " | Total /40 | Verdict |"
    sep = "|" + "---|" * (len(DIMS) + 3)
    print(head)
    print(sep)
    for i in data["ideas"]:
        cells = []
        for k, _ in DIMS:
            c = str(i["scores"][k])
            if k == "fmf" and i.get("fmf_unscored"):
                c += "*"
            cells.append(c)
        print(f"| {i['name']} | " + " | ".join(cells) + f" | **{i['total']}** | {i['verdict']} |")
    print()
    for i in data["ideas"]:
        extra = f" ({'; '.join(i['gate_notes'])})" if i["gate_notes"] else ""
        print(f"- {i['name']}: weakest = {i['weakest']}{extra}")
    if any(i.get("fmf_unscored") for i in data["ideas"]):
        print("\n\\* Founder Fit unscored (no background given), set to a neutral 3.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
