# AEGIS lab sandbox — Docker

This directory stands up the **only authorised attack target** for AEGIS:
[OWASP Juice Shop](https://owasp.org/www-project-juice-shop/), a deliberately
insecure web application, running locally in Docker.

## Prerequisites
- Docker Engine + Docker Compose v2 (`docker compose version`).

## Start / stop
```bash
docker compose up -d        # pull image + start in background
docker compose ps           # check it's healthy
docker compose logs -f      # watch startup
docker compose down         # stop and remove the container
```

Once healthy, open **http://localhost:3000**.

## Port
- Default host port: **3000** (bound to `127.0.0.1` only).
- To change it, edit the `ports:` mapping in `docker-compose.yml`, e.g.
  `"127.0.0.1:3001:3000"` to serve on host port 3001. If you change it, update
  `AEGIS_TARGET_URL` in `attacker/.env`.

## Safety notes
- The container is bound to **loopback (`127.0.0.1`)**, so it is not reachable from
  other machines on your network.
- `NODE_ENV=unsafe` deliberately enables all challenges — appropriate for a *local*
  teaching lab, **never** for anything internet-facing.
- This is the only host AEGIS tooling should ever point at. See the root `README.md`
  legal/ethics notice (UK Computer Misuse Act 1990).

## Pinning (recommended)
For a reproducible dissertation build, pin a specific version instead of `:latest`,
e.g. `bkimminich/juice-shop:v17.1.1`, and record the digest.
