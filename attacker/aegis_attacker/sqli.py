"""SQL injection phase (stub).

SCAFFOLD: the LLM proposes SQLi payloads for endpoints found in recon; each
attempt is executed against the LAB ONLY and an event is emitted.
"""
from __future__ import annotations

from .config import Config
from .events import emit, new_event


def run(cfg: Config, recon_events: list[dict]) -> list[dict]:
    """Attempt SQLi against recon findings (stubbed)."""
    # TODO: ask Groq for payloads; send via requests; classify the response.
    ev = new_event(
        match_id=cfg.match_id,
        actor="attacker",
        phase="sqli",
        action="sqli_attempt",
        target=f"{cfg.target_url}/rest/products/search",
        outcome="success",
        severity="high",
        summary="[stub] SQLi payload on search param returned unexpected rows.",
        detail={"param": "q", "payload": "'))--", "stub": True},
    )
    emit(cfg.event_log, ev)
    return [ev]
