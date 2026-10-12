#!/usr/bin/env python3
"""Check that every recorded harness failure actually landed in its canonical file."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "harness/failures.jsonl"

REQUIRED = ("id", "date", "symptom", "cause", "form", "status")
FORMS = {"check", "asset", "gotcha", "contract", "rule"}
STATUSES = {"open", "landed", "wont-fix"}


def read_entries(path):
    entries = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        try:
            entries.append((number, json.loads(line)))
        except json.JSONDecodeError as error:
            raise ValueError(f"line {number}: invalid JSON ({error})") from error
    return entries


def problems_for(number, entry):
    found = []
    missing = [field for field in REQUIRED if not entry.get(field)]
    if missing:
        found.append(f"missing {', '.join(missing)}")
        return found
    if entry["status"] not in STATUSES:
        found.append(f"status must be one of {sorted(STATUSES)}")
    if entry["form"] not in FORMS:
        found.append(f"form must be one of {sorted(FORMS)}")
    if entry["status"] == "open":
        found.append("still open: land it in a canonical file or mark wont-fix with a note")
    if entry["status"] == "wont-fix" and not entry.get("note"):
        found.append("wont-fix needs a note explaining why")
    if entry["status"] == "landed":
        canonical, anchor = entry.get("canonical"), entry.get("anchor")
        if not canonical or not anchor:
            found.append("landed needs canonical and anchor")
        elif Path(canonical).is_absolute():
            found.append("canonical must be relative to the repo root or start with ~/")
        else:
            # ~/ points outside the repo, e.g. the global harness-design skill
            target = (Path(canonical).expanduser() if canonical.startswith("~/") else ROOT / canonical).resolve()
            if not target.is_file():
                found.append(f"canonical file not found: {canonical}")
            elif anchor not in target.read_text(encoding="utf-8"):
                found.append(f"anchor not present in {canonical}: {anchor!r}")
    return found


def main(argv):
    ledger = Path(argv[1]) if len(argv) > 1 else DEFAULT_LEDGER
    if not ledger.is_file():
        print(f"SKIPPED: no ledger at {ledger}", flush=True)
        return 0
    entries = read_entries(ledger)
    if not entries:
        print("SKIPPED: ledger is empty", flush=True)
        return 0
    failures = 0
    counts = {}
    for number, entry in entries:
        counts[entry.get("status", "?")] = counts.get(entry.get("status", "?"), 0) + 1
        for problem in problems_for(number, entry):
            print(f"FAILED line {number} [{entry.get('id', '?')}]: {problem}", file=sys.stderr, flush=True)
            failures += 1
    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"harness ledger: {len(entries)} entries ({summary})", flush=True)
    return int(failures > 0)


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except (OSError, ValueError) as error:
        print(f"Invalid harness ledger: {error}", file=sys.stderr)
        sys.exit(1)
