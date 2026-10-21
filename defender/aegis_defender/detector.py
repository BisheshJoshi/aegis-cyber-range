"""Detect + block pipeline (stub).

SCAFFOLD: the defender watches attacker events and scores them for maliciousness.
In the full version this is an ML model (e.g. TF-IDF over request payloads + a
classifier) trained on benign vs. attack traffic. On a positive detection it emits
a `detect` event and then a `block` event — blocking happens FIRST, before any
patching. Here we use a trivial keyword heuristic as a placeholder.
"""
from __future__ import annotations

from typing import Any

from .events import emit, new_event

# Placeholder signatures; the real detector replaces this with a trained model.
_SQLI_MARKERS = ("'", "--", " or ", "))", "union", "select")
_XSS_MARKERS = ("<script", "onerror=", "javascript:", "alert(")


def score_event(event: dict[str, Any]) -> tuple[bool, str, float]:
    """Return (is_malicious, kind, score). SCAFFOLD heuristic — replace with ML."""
    payload = str((event.get("detail") or {}).get("payload", "")).lower()
    if any(m in payload for m in _SQLI_MARKERS) or event.get("phase") == "sqli":
        return True, "sqli", 0.94
    if any(m in payload for m in _XSS_MARKERS) or event.get("phase") == "xss":
        return True, "xss", 0.88
    return False, "none", 0.02


def handle(cfg, event: dict[str, Any]) -> list[dict]:
    """Detect, then block. Returns emitted defender events."""
    emitted: list[dict] = []
    is_mal, kind, score = score_event(event)
    if not is_mal:
        return emitted

    detect = new_event(
        match_id=cfg.match_id, phase="detect", action="anomaly_detected",
        target=event.get("target", cfg.target_url), outcome="detected",
        severity="high",
        summary=f"[stub] Detected {kind.upper()} pattern (score={score}).",
        detail={"kind": kind, "score": score, "model": "stub-heuristic"},
        refs=[event["event_id"]],
    )
    emit(cfg.event_log, detect); emitted.append(detect)

    block = new_event(
        match_id=cfg.match_id, phase="block", action="attack_blocked",
        target=event.get("target", cfg.target_url), outcome="blocked",
        severity="high",
        summary=f"[stub] Blocked {kind.upper()} request before response.",
        refs=[event["event_id"]],
    )
    emit(cfg.event_log, block); emitted.append(block)
    return emitted
