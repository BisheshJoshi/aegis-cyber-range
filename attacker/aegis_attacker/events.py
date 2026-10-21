"""Tiny event-emitter used by the attacker.

SCAFFOLD: appends schema-conformant events (see events/SCHEMA.md) as JSON lines.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

SCHEMA_VERSION = "1.0"


def new_event(
    *,
    match_id: str,
    actor: str,
    phase: str,
    action: str,
    target: str,
    outcome: str,
    summary: str,
    severity: str | None = None,
    detail: dict[str, Any] | None = None,
    refs: list[str] | None = None,
) -> dict[str, Any]:
    """Build one event envelope (see events/SCHEMA.md)."""
    event: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "event_id": str(uuid.uuid4()),
        "match_id": match_id,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "actor": actor,
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
    """Append one event as a JSON line, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")
    return event
