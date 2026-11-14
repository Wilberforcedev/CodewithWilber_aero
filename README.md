# Code with Wilber

A course discovery and learning-path website built with Python, FastAPI, Jinja, and SQLAlchemy. The interface takes cues from modern creator-led course platforms: clear course outcomes, focused learning paths, and simple calls to action. All copy and visual identity here are original.

## Features

- Responsive home page with course discovery, learning paths, and an instructor introduction.
- Searchable course catalogue with category filters.
- Course and learning-path detail pages.
- SQLite for local development and PostgreSQL in the supplied Docker Compose setup.
- Health endpoint, security response headers, structured application logging, and environment-based settings.
- Container runs as an unprivileged user.

## Run locally

Requires Python 3.12 or later.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Open <http://localhost:8000>. The starter catalogue is seeded automatically after the database migration has run.

## Run with Docker

```bash
docker compose up --build
```

Set a unique `POSTGRES_PASSWORD` and the production `SITE_URL` before deploying. For production, terminate TLS at a trusted reverse proxy, set `ENVIRONMENT=production`, and use a managed PostgreSQL service with backups and restricted network access.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_NAME` | Site name | `Code with Wilber` |
| `ENVIRONMENT` | `development` or `production` | `development` |
| `DATABASE_URL` | SQLAlchemy URL | `sqlite:///./wilber.db` |
| `SITE_URL` | Canonical origin used by metadata and sitemap | `http://localhost:8000` |
| `CONTACT_EMAIL` | Contact address shown on the site | `hello@codewithwilber.com` |
| `CHECKOUT_URL` | Optional checkout destination for course CTAs | unset |
| `LOG_LEVEL` | Python log level | `INFO` |

## Routes

- `/` — landing page
- `/courses` — course catalogue (`?q=python&category=Python`)
- `/courses/{slug}` — course detail
- `/learning-paths` and `/learning-paths/{slug}` — curated paths
- `/health` — liveness and database readiness
- `/robots.txt` and `/sitemap.xml` — crawler metadata

Course data is seeded only when the catalogue is empty. Replace the starter records in `app/catalog.py` with verified course descriptions, instructor details, pricing, and genuine testimonials before opening the site to customers. Payment processing, student accounts, and video hosting are intentionally left for integration with the chosen providers. Schema changes are managed with Alembic; apply migrations as a release step before serving traffic.

## Operations

Use a database migration tool before changing the schema on an existing production database. Keep secrets outside source control, configure backups and monitoring, and review reverse-proxy settings before enabling forwarded headers. This repository is a deployable application foundation, not a claim that payment, identity, or course delivery integrations have been configured.

