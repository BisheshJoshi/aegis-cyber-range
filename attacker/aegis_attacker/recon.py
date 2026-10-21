"""Recon phase (stub).

SCAFFOLD: in the full implementation, the Groq LLM is prompted to enumerate the
lab target's surface (endpoints, parameters, reflected inputs) and pick candidate
injection points. Here we emit a single placeholder recon event.
"""
from __future__ import annotations

from .config import Config
from .events import emit, new_event


def run(cfg: Config) -> list[dict]:
    """Return the list of events emitted during recon (stubbed)."""
    # TODO: call Groq to plan recon; use requests to probe cfg.target_url safely.
    ev = new_event(
        match_id=cfg.match_id,
        actor="attacker",
        phase="recon",
        action="endpoint_discovered",
        target=f"{cfg.target_url}/rest/products/search",
        outcome="success",
        severity="low",
        summary="[stub] Recon identified a candidate reflected search endpoint.",
        detail={"method": "GET", "param": "q", "stub": True},
    )
    emit(cfg.event_log, ev)
    return [ev]
