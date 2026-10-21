"""AEGIS defender entrypoint (stub orchestration).

Reads the shared event log and runs: detect -> block (first) -> patch -> verify.
By default it processes events already written by the attacker; pass --tail to
follow the log live.

    python main.py          # one pass over existing events
    python main.py --tail   # follow the log

SCAFFOLD: detection is a placeholder heuristic; patch/verify are simulated.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

from aegis_defender.events import read_events, tail_events
from aegis_defender import detector, responder

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


@dataclass(frozen=True)
class DefenderConfig:
    match_id: str
    target_url: str
    event_log: str

    @staticmethod
    def from_env() -> "DefenderConfig":
        return DefenderConfig(
            match_id=os.getenv("AEGIS_MATCH_ID", "demo-match-001"),
            target_url=os.getenv("AEGIS_TARGET_URL", "http://localhost:3000"),
            event_log=os.getenv(
                "AEGIS_EVENT_LOG", "../events/runtime/match-demo-match-001.jsonl"
            ),
        )


def _process(cfg: DefenderConfig, event: dict) -> None:
    # Only react to attacker events (avoid reacting to our own output).
    if event.get("actor") != "attacker":
        return
    emitted = detector.handle(cfg, event)
    if emitted:
        _, kind, _ = detector.score_event(event)
        responder.respond(cfg, event, kind)


def main() -> None:
    cfg = DefenderConfig.from_env()
    follow = "--tail" in sys.argv
    print(f"[AEGIS defender] match={cfg.match_id} log={cfg.event_log} tail={follow}")

    if follow:
        for event in tail_events(cfg.event_log):
            _process(cfg, event)
    else:
        for event in read_events(cfg.event_log):
            _process(cfg, event)
        print("[AEGIS defender] processed existing events (stub). Done.")


if __name__ == "__main__":
    main()
