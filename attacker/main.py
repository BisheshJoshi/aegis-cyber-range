"""AEGIS attacker entrypoint (stub orchestration).

Runs the campaign phases in order: recon -> SQLi -> XSS, against the LOCAL lab
target only. Emits events to the shared event log for the defender and game layer.

    python main.py

SCAFFOLD: phases are stubs; no real attacks are performed yet.
"""
from __future__ import annotations

from aegis_attacker.config import Config
from aegis_attacker import recon, sqli, xss
from aegis_attacker.events import emit, new_event


def main() -> None:
    cfg = Config.from_env()  # raises if target is not the local lab
    print(f"[AEGIS attacker] target={cfg.target_url} match={cfg.match_id}")
    print(f"[AEGIS attacker] event log -> {cfg.event_log}")

    emit(
        cfg.event_log,
        new_event(
            match_id=cfg.match_id, actor="system", phase="info",
            action="match_started", target=cfg.target_url, outcome="info",
            severity="info", summary="AEGIS attacker campaign started (scaffold).",
        ),
    )

    recon_events = recon.run(cfg)
    sqli.run(cfg, recon_events)
    xss.run(cfg, recon_events)

    print("[AEGIS attacker] campaign complete (stub). See the event log.")


if __name__ == "__main__":
    main()
