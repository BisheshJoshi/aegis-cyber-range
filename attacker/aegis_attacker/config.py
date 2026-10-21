"""Attacker configuration + safety guard rails.

SCAFFOLD: loads settings from the environment (.env via python-dotenv) and
enforces the single most important rule of this project: we only ever attack the
local sandbox lab. See the root README legal/ethics note (UK Computer Misuse Act 1990).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv  # python-dotenv
    load_dotenv()
except Exception:  # pragma: no cover - dotenv optional at runtime
    pass

# Hosts we consider "the lab". The sandbox binds to loopback only.
_ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"}


class UnsafeTargetError(RuntimeError):
    """Raised when a target is not the local sandbox lab."""


@dataclass(frozen=True)
class Config:
    groq_api_key: str
    groq_model: str
    target_url: str
    match_id: str
    event_log: str

    @staticmethod
    def from_env() -> "Config":
        target = os.getenv("AEGIS_TARGET_URL", "http://localhost:3000")
        Config._assert_lab_target(target)
        return Config(
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            target_url=target,
            match_id=os.getenv("AEGIS_MATCH_ID", "demo-match-001"),
            event_log=os.getenv(
                "AEGIS_EVENT_LOG", "../events/runtime/match-demo-match-001.jsonl"
            ),
        )

    @staticmethod
    def _assert_lab_target(url: str) -> None:
        """Refuse anything that is not the loopback lab. DO NOT weaken this."""
        host = (urlparse(url).hostname or "").lower()
        if host not in _ALLOWED_HOSTS:
            raise UnsafeTargetError(
                f"Refusing non-lab target {url!r}. AEGIS may only attack the local "
                f"sandbox ({', '.join(sorted(_ALLOWED_HOSTS))}). "
                f"Attacking other systems without authorisation is illegal "
                f"(UK Computer Misuse Act 1990)."
            )

    def require_groq_key(self) -> str:
        if not self.groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy attacker/.env.example to .env and add "
                "your free Groq key (https://console.groq.com/keys)."
            )
        return self.groq_api_key
