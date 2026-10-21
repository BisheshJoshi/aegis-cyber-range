# AEGIS Event Log — Schema

AEGIS components communicate through a single, append-only **event log**: a
[JSON Lines](https://jsonlines.org/) file (`*.jsonl`) where **each line is one JSON
object** conforming to `event.schema.json`. The LLM attacker and the ML defender both
**emit** events; the game/visualisation layer **consumes** them.

Keeping the contract simple (flat, documented, one object per line) makes it trivial to
tail in real time, diff, replay, and render.

## Default location
At runtime, components write to `events/runtime/match-<id>.jsonl` (git-ignored).
`example-events.jsonl` in this folder is a committed sample for docs/tests.

## Event envelope (all events share these fields)

| Field         | Type     | Required | Description |
|---------------|----------|----------|-------------|
| `schema_version` | string | yes | Schema version, e.g. `"1.0"`. |
| `event_id`    | string (uuid) | yes | Unique id for this event. |
| `match_id`    | string   | yes | Groups all events in one attacker-vs-defender run. |
| `ts`          | string (ISO-8601, UTC) | yes | When the event occurred, e.g. `2026-10-21T00:00:00Z`. |
| `actor`       | enum     | yes | `attacker` \| `defender` \| `system`. |
| `phase`       | enum     | yes | `recon` \| `sqli` \| `xss` \| `detect` \| `block` \| `patch` \| `verify` \| `info`. |
| `action`      | string   | yes | Short machine name of what happened, e.g. `sqli_attempt`, `attack_blocked`. |
| `target`      | string   | yes | Target URL/endpoint. **Must be the lab** (`http://localhost:<port>` / loopback). |
| `outcome`     | enum     | yes | `success` \| `failure` \| `blocked` \| `detected` \| `patched` \| `verified` \| `info`. |
| `severity`    | enum     | no  | `info` \| `low` \| `medium` \| `high` \| `critical`. |
| `summary`     | string   | yes | Human-readable one-line description (safe for the game UI). |
| `detail`      | object   | no  | Free-form, phase-specific structured data (payload, endpoint, model scores, patch id…). |
| `refs`        | array[string] | no | `event_id`s this event responds to (e.g. a defender `detect` referencing an attacker `sqli` event). |

### Conventions
- **Time** is always UTC ISO-8601 with a trailing `Z`.
- **`target`** must be loopback/lab — consumers may reject non-lab targets.
- **`detail`** is intentionally open so phases can carry what they need without schema churn;
  put anything stable and queryable in top-level fields.
- Attacker phases: `recon → sqli → xss`. Defender phases: `detect → block → patch → verify`.
- The defender links its response to the triggering attacker event via `refs`.

## Example lifecycle (one SQLi exchange)
1. attacker `recon` / `endpoint_discovered`
2. attacker `sqli` / `sqli_attempt` → `outcome: success`
3. defender `detect` / `anomaly_detected` (`refs` the sqli event)
4. defender `block` / `attack_blocked`
5. defender `patch` / `patch_applied`
6. defender `verify` / `patch_verified`

See `example-events.jsonl` for the concrete JSON.
