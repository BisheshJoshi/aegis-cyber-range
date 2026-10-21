"""Patch + verify pipeline (stub).

SCAFFOLD: AFTER an attack is blocked, the defender applies a (virtual) patch for
the weakness and then verifies it by replaying the attack and confirming it now
fails. Emits `patch` then `verify` events.
"""
from __future__ import annotations

from typing import Any

from .events import emit, new_event


def respond(cfg, trigger_event: dict[str, Any], kind: str) -> list[dict]:
    """Apply a patch then verify it. Returns emitted defender events."""
    emitted: list[dict] = []

    patch = new_event(
        match_id=cfg.match_id, phase="patch", action="patch_applied",
        target=trigger_event.get("target", cfg.target_url), outcome="patched",
        severity="medium",
        summary=f"[stub] Applied virtual patch for {kind.upper()}.",
        detail={"patch_id": f"vp-{kind}-001", "type": "virtual-patch"},
        refs=[trigger_event["event_id"]],
    )
    emit(cfg.event_log, patch); emitted.append(patch)

    # TODO: actually replay the payload against the lab and confirm failure.
    verify = new_event(
        match_id=cfg.match_id, phase="verify", action="patch_verified",
        target=trigger_event.get("target", cfg.target_url), outcome="verified",
        severity="info",
        summary=f"[stub] Replay confirms {kind.upper()} no longer succeeds.",
        refs=[patch["event_id"]],
    )
    emit(cfg.event_log, verify); emitted.append(verify)
    return emitted
