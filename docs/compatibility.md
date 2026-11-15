# Firecrawl v2 compatibility subset

Base: `/compat/firecrawl/v2`. Authentication uses your HoundCrawler bearer key.

Supported: POST `/scrape`, POST `/crawl`, POST `/batch/scrape`, GET/DELETE `/crawl/{id}` and `/batch/scrape/{id}`. Result pages contain a `next` URL when another cursor page may exist; an empty final page is possible.

String formats only. Supported scrape options: formats, onlyMainContent, includeTags, excludeTags, maxAge (milliseconds, rounded down to seconds), timeout (milliseconds). Supported crawl options: url/urls, limit, maxDiscoveryDepth, scrapeOptions, sitemap, ignoreQueryParameters, allowSubdomains, allowExternalLinks, crawlEntireDomain, maxConcurrency. Unknown options fail explicitly. Native path rules are globs; compatibility regex includePaths/excludePaths are rejected to avoid silently changing their meaning.

Synchronous map, object formats, provider-specific proxies, sessions, search, hosted credits and webhook shapes are not Firecrawl-compatible. Use native asynchronous POST `/v1/map`. Native max_pages counts sitemap/error resources as well as HTML, unlike a successful-document-only limit. No Firecrawl implementation code is included.
