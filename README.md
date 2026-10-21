# AEGIS — An AI-Driven Cyber-Range for Teaching Security Concepts

> Final-year BSc Computer Science project — University (UK).
> **Author:** Bishesh Joshi

AEGIS is a self-contained, locally-hosted cyber-range that teaches offensive and
defensive security concepts through an *autonomous attacker vs. autonomous defender*
loop running against a **sandboxed, intentionally-vulnerable lab target**. A thin
game/visualisation layer turns the resulting event stream into a teaching experience.

---

## ⚖️ Legal & Ethics Notice — READ FIRST

**This project targets ONLY the sandboxed lab container it ships with (OWASP Juice Shop,
running on `localhost`). It must NEVER be pointed at any system you do not own or do not
have explicit written authorisation to test.**

In the UK, unauthorised access to or interference with computer systems is a criminal
offence under the **Computer Misuse Act 1990** (notably ss. 1–3A), carrying penalties up
to imprisonment. Running automated recon, SQL injection, XSS, or any other attack tooling
against third-party websites, cloud services, or networks **without authorisation is
illegal**, regardless of intent or educational purpose.

By design, AEGIS:
- Ships its own deliberately-vulnerable target (OWASP Juice Shop) in Docker.
- Defaults every attacker target to `http://localhost:<port>` (the lab container only).
- Includes guard rails/stubs intended to refuse non-loopback, non-lab targets.

**You are solely responsible for how you use this software. Attack the lab, nothing else.**

---

## 💸 £0 Stack

AEGIS is built to run entirely on free tiers / open-source software:

| Component            | Tool / Service                         | Cost |
|----------------------|----------------------------------------|------|
| Lab target           | OWASP Juice Shop (`bkimminich/juice-shop`, Docker) | Free / OSS |
| Sandbox orchestration| Docker + Docker Compose                | Free / OSS |
| LLM attacker brain   | Groq API (free tier)                   | £0 (free tier) |
| ML defender          | Python + scikit-learn (local)          | Free / OSS |
| Event log            | Local JSON lines file                  | Free |
| Game/visualisation layer (future) | Next.js on Vercel (free tier) + Supabase (free tier) | £0 (free tiers) |

No paid infrastructure is required to develop or demo the project.

---

## 🏗️ Architecture Overview

```
                      ┌──────────────────────────────────────────────┐
                      │                 AEGIS Cyber-Range             │
                      │                                              │
  ┌───────────────┐   │   ┌────────────────┐        attacks         │
  │  Game / Viz   │   │   │  LLM Attacker  │  ───────────────────┐   │
  │  layer        │◀──┼───│  (Groq free)   │                     │   │
  │ (Vercel +     │   │   │  recon → sqli  │                     ▼   │
  │  Supabase)    │   │   │        → xss   │            ┌────────────────────┐
  └───────▲───────┘   │   └───────▲────────┘            │  Lab Target (Docker)│
          │           │           │                     │  OWASP Juice Shop   │
          │ reads     │           │ emit events         │  localhost:3000     │
          │           │           │                     └────────▲───────────┘
   ┌──────┴────────┐  │   ┌───────┴────────┐  observes / blocks   │
   │  Event Log    │◀─┼───│  ML Defender   │ ─────────────────────┘
   │ (events/*.jsonl)│ │   │ detect → block │
   └───────────────┘  │   │ → patch → verify│
                      │   └────────────────┘
                      └──────────────────────────────────────────────┘
```

### Flow
1. **Sandbox** — `docker/docker-compose.yml` stands up OWASP Juice Shop on a local port
   (default **3000**). This is the *only* authorised target.
2. **LLM Attacker** (`attacker/`) — uses the Groq free tier to plan and run a campaign:
   **recon** (enumerate endpoints/surface) → **SQLi** attempts → **XSS** attempts. Each
   step emits a structured JSON event.
3. **ML Defender** (`defender/`) — consumes the event stream and runs a pipeline:
   **detect → block** the attack *first*, then **patch** the simulated weakness and
   **verify** the patch held. Emits its own events.
4. **Event Log** (`events/`) — a simple, documented JSON schema both sides emit. The
   game/visualisation layer consumes it to render the attacker-vs-defender match.

### Repository layout
```
aegis-cyber-range/
├── README.md               # this file
├── LICENSE                 # MIT
├── CONTRIBUTING.md         # how to work on the project (optional/short)
├── .gitignore
├── docker/                 # sandbox lab target
│   ├── docker-compose.yml  # OWASP Juice Shop
│   └── README.md
├── attacker/               # Groq-powered LLM attacker (Python)
│   ├── aegis_attacker/
│   │   ├── __init__.py
│   │   ├── config.py       # reads GROQ_API_KEY + target from env
│   │   ├── events.py       # event-emitter helper
│   │   ├── recon.py        # recon stub
│   │   ├── sqli.py         # SQL injection attack stub
│   │   └── xss.py          # XSS attack stub
│   ├── main.py             # orchestration entrypoint (stub)
│   ├── requirements.txt    # groq, requests, python-dotenv
│   └── .env.example
├── defender/               # ML defender (Python)
│   ├── aegis_defender/
│   │   ├── __init__.py
│   │   ├── detector.py     # detect/block pipeline stub
│   │   ├── responder.py    # patch/verify stub
│   │   └── events.py       # reads/writes the event log
│   ├── main.py             # orchestration entrypoint (stub)
│   └── requirements.txt    # scikit-learn, etc.
└── events/                 # shared event-log contract
    ├── SCHEMA.md           # human docs for the schema
    ├── event.schema.json   # JSON Schema
    └── example-events.jsonl# sample events
```

---

## 🚀 Quick start (development)

> ⚠️ Scaffold only — modules are commented stubs. Nothing attacks anything yet.

```bash
# 1. Stand up the lab target
cd docker
docker compose up -d           # Juice Shop → http://localhost:3000

# 2. Configure the attacker
cd ../attacker
cp .env.example .env           # then paste your Groq free-tier API key
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py                 # runs the (stubbed) recon→sqli→xss campaign

# 3. Run the defender (separate shell)
cd ../defender
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py                 # tails the event log, detect→block→patch→verify
```

---

## 🗺️ Roadmap (indicative)
- **Level 1 (core):** Juice Shop target, recon + SQLi + XSS attacker, detect/block/patch/verify defender, JSON event log. *(this scaffold)*
- **Level 2+:** additional lab targets, richer ML detection models, scoring.
- **Game layer:** Next.js (Vercel) + Supabase reading the event log; live match visualisation.

## 📄 License
MIT — see [LICENSE](LICENSE).
