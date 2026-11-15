# HoundCrawler

**Durable web crawling and clean source content for AI agents.**

[![Checks](https://github.com/warhoundai/HoundCrawler/actions/workflows/checks.yml/badge.svg)](https://github.com/warhoundai/HoundCrawler/actions/workflows/checks.yml)
[![Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-black)](LICENSE)

HoundCrawler crawls, maps and batches public pages into text, Markdown, links, metadata and evidence-bearing artifacts. PostgreSQL keeps the frontier, reservations, leases, checkpoints and result cursors durable across worker restarts. It runs on your infrastructure with your own optional provider keys.

**0.1.0rc1 is a measured preview.** It is not a claim of Firecrawl parity. Read [capabilities](docs/capabilities.md), [compatibility](docs/compatibility.md) and the [verification record](docs/verification.md) for tested boundaries.

## Run locally

Requires Python 3.12+ and Docker Compose. No paid API key is needed for HTTP crawling.

```bash
git clone https://github.com/warhoundai/HoundCrawler.git
cd HoundCrawler
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.lock
python scripts/configure.py
docker compose up --build -d
```

The generated `.env` contains your instance credentials. Load them locally with `set -a; . ./.env; set +a`, then use the API key from `HOUNDCRAWLER_API_KEYS`. Never commit this file. API binds to `127.0.0.1:8081`; put TLS and an authenticated gateway in front of remote installations.

```bash
curl http://127.0.0.1:8081/v1/crawl \
  -H "Authorization: Bearer $HOUNDCRAWLER_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"urls":["https://example.com/"],"max_pages":100,"sitemap":"include","options":{"formats":["markdown","text"],"render":"never"}}'
```

Set `HOUNDCRAWLER_API_KEY` yourself to a tenant key from the generated JSON. The response contains a durable job ID. Poll `GET /v1/jobs/{id}` and page `GET /v1/jobs/{id}/results?cursor=0`; continue with `next_cursor`. API schemas are authenticated at `/v1/openapi.json`.

## Capabilities

- Crawl, map, batch and single-page acquisition; scoped sitemap and gzip discovery, glob paths, domain/subdomain controls and query deduplication.
- Distributed leases, per-job concurrency, per-origin serialization and pacing, bounded decoding, Retry-After handling, retries, pause/resume/cancel, SSE and signed webhooks.
- Tenant-bound credentials and artifacts; public-DNS pinning, redirect policy, no arbitrary shell or CDP access.
- Optional isolated Chromium rendering and document/media parser. Optional structured extraction uses your own explicitly configured model.
- Python SDK, JavaScript SDK, CLI and MCP stdio adapter. Agents call the API; they do not get internal service access.

```python
from houndcrawler.client import Client
with Client('https://your-crawler.example', api_key='your-instance-key') as client:
    job = client.submit('crawl', ['https://example.com/'], max_pages=100)
    client.wait(job['id'])
    for page in client.results(job['id']):
        print(page['url'], page.get('data', {}).get('markdown'))
```

See [API](docs/api.md), [self-hosting](docs/deployment.md), [architecture](docs/architecture.md), [MCP and optional integrations](docs/advanced.md), [security](SECURITY.md), [contributing](CONTRIBUTING.md) and [license](LICENSE).

## Relationship to other projects

This is a separate Apache-2.0 product derived from the public HoundScraper core at the commit recorded in [PROVENANCE.json](PROVENANCE.json). HoundScraper and its existing APIs remain unchanged. HoundSearch uses this public core for retrieval and indexing. HoundExtract, HoundX and WarHoundAI are separate proprietary projects and are not included.
