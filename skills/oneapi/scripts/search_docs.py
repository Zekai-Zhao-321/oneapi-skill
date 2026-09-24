#!/usr/bin/env python3
"""Bounded, offline ranked search. Python 3.10+, standard library only."""
import argparse
import json
import math
from pathlib import Path
import re

DOCS = Path(__file__).resolve().parents[1] / "docs"
STOP = {"a", "an", "the", "how", "do", "i", "to", "for", "of", "in", "and", "is", "with", "what", "does"}


def search(query, project=None, kind="doc", limit=8):
    catalog = json.loads((DOCS / "catalog.json").read_text())
    projects = {e["project"] for e in catalog}
    if project and project not in projects:
        raise ValueError(f"Unknown project {project!r}; choose: " + ", ".join(sorted(projects)))
    tokens = list(dict.fromkeys(t for t in re.findall(r"[a-z0-9_]+", query.lower()) if t not in STOP))
    if not tokens:
        raise ValueError("Query needs at least one searchable word")
    phrase = query.lower().strip()
    matches = []
    for entry in catalog:
        if (project and entry["project"] != project) or (kind != "all" and entry["kind"] != kind):
            continue
        if entry["kind"] == "license":
            continue
        content = (DOCS / entry["path"]).read_text(errors="replace")
        lower = content.lower()
        heading = (entry["source_path"] + " " + entry["title"]).lower()
        hits = [t for t in tokens if t in lower or t in heading]
        if not hits:
            continue
        # Rank coverage first, exact phrase/title next. Length normalization keeps
        # giant generated headers from burying focused reference pages.
        score = 20 * len(hits) / len(tokens)
        score += sum(4 for t in tokens if t in heading)
        score += 12 if phrase in heading else 0
        score += 8 if phrase in lower else 0
        score += sum(math.log1p(lower.count(t)) for t in hits) / (1 + math.log1p(len(content)) / 10)
        lines = content.splitlines()
        line_scores = [(sum(t in line.lower() for t in tokens) + 2 * (phrase in line.lower()), i)
                       for i, line in enumerate(lines)]
        _, index = max(line_scores, key=lambda item: (item[0], -item[1]), default=(0, 0))
        snippet = "\n".join(f"{i + 1}: {lines[i][:240]}" for i in range(max(0, index - 1), min(len(lines), index + 2)))
        matches.append(dict(path=entry["path"], title=entry["title"], project=entry["project"],
                            kind=entry["kind"], score=round(score, 3), line=index + 1, snippet=snippet))
    return sorted(matches, key=lambda e: (-e["score"], e["path"]))[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?")
    parser.add_argument("--project")
    parser.add_argument("--kind", choices=["doc", "api", "example", "support", "all"], default="doc")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--list-projects", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be between 1 and 50")
    try:
        if args.list_projects:
            print("\n".join(sorted({e["project"] for e in json.loads((DOCS / "catalog.json").read_text())})))
            return
        if not args.query:
            parser.error("query is required unless --list-projects is used")
        results = search(args.query, args.project, args.kind, args.limit)
        if args.json:
            print(json.dumps(results, indent=2))
        elif results:
            for result in results:
                print(f"docs/{result['path']}:{result['line']} — {result['title']}\n{result['snippet']}\n")
        else:
            print("No matches. Try a shorter symbol, a different project, or --kind all.")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"search failed: {exc}\n")


if __name__ == "__main__":
    main()
