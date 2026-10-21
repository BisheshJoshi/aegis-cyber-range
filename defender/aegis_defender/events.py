"""Event-log I/O for the defender.

SCAFFOLD: reads the attacker's JSON-lines events and appends the defender's own
events (same contract, see events/SCHEMA.md).
"""
from __future__ import annotations

import json
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Iterator

SCHEMA_VERSION = "1.0"


def read_events(log_path: str) -> list[dict[str, Any]]:
    """Read all events currently in the log (empty list if missing)."""
    if not os.path.exists(log_path):
        return []
    out: list[dict[str, Any]] = []
    with open(log_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def tail_events(log_path: str, poll_s: float = 1.0) -> Iterator[dict[str, Any]]:
    """Yield new events as they are appended (simple polling tail).

    SCAFFOLD: good enough for a local demo; swap for watchdog/inotify later.
    """
    pos = 0
    while True:
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as fh:
                fh.seek(pos)
                for line in fh:
                    line = line.strip()
                    if line:
                        yield json.loads(line)
                pos = fh.tell()
        time.sleep(poll_s)


def new_event(
    *,
    match_id: str,
    phase: str,
    action: str,
    target: str,
    outcome: str,
    summary: str,
    severity: str | None = None,
    detail: dict[str, Any] | None = None,
    refs: list[str] | None = None,
) -> dict[str, Any]:
    """Build a defender event envelope (actor fixed to 'defender')."""
    event: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "event_id": str(uuid.uuid4()),
        "match_id": match_id,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "actor": "defender",
        "phase": phase,
        "action": action,
        "target": target,
        "outcome": outcome,
        "summary": summary,
    }
    if severity:
        event["severity"] = severity
    if detail:
        event["detail"] = detail
    if refs:
        event["refs"] = refs
    return event


def emit(log_path: str, event: dict[str, Any]) -> dict[str, Any]:
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")
    return event
