# Capabilities and boundaries

Version 0.1.0rc1 is a measured preview. Core tests exercise persistent jobs, tenant isolation, byte/model reservations, HTTP decoding and redirects, credentials, cancellation and acquisition. See verification.md for actual results; optional-profile skips are not passes.

Crawl/map/batch expose a PostgreSQL frontier, public-DNS-pinned HTTP, sitemap indexes and bounded gzip, glob include/exclude paths, optional subdomains/external links, query deduplication, concurrency, origin pacing, retry/backoff, pause/resume/cancel, cursor results, SSE and webhooks. Robots rules are respected by default. Operators can configure an explicit override for authorized use.

A page budget counts frontier resources, including sitemap documents and failed pages, not just successful HTML pages. Time, bytes and concurrency are explicit per-job operator budgets and are resumable. Sitemap discovery cannot find unlinked or authenticated resources without seed URLs and configured credentials. No crawler can guarantee every page of an arbitrary website.

Core formats: text, Markdown, HTML, links, images, metadata, tables, JSON-LD and attributes. Browser formats require the optional isolated signed Chromium worker distributed here. The standalone HoundBrowser session API is a different protocol; this release does not silently treat it as compatible. Browser execution is isolated by process/container, not a complete multi-tenant kernel security boundary: deploy separate workers or stronger isolation for hostile workloads.

Binary documents and OCR/media need the optional parser image and explicitly provisioned models. Model extraction needs your provider and pricing configuration. These are not enabled in the default HTTP profile. No rotating residential proxy service, CAPTCHA bypass network, Firecrawl account, or production WarHound credential is included.

Caching is TTL-based; conditional ETag/Last-Modified recrawl is not claimed in this preview. Firecrawl compatibility is an explicit subset, not a drop-in replacement. No unmeasured production SLA or external competitor parity is asserted.
