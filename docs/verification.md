# Verification record

Local core suite: **52 passed**, with six optional-profile tests and the opt-in scale test skipped in the default local run. New scope/query/sitemap and hard per-job concurrency checks pass. Existing real HTTP, tenant-isolation, reservation and recovery tests are included.

GitHub core, JavaScript, dashboard/browser, dependency audit, package build and container smoke gates passed at commit eed3614a1fc27fb0829c3bda04fa000292c4de15: https://github.com/warhoundai/HoundCrawler/actions/runs/43692868354 .

The separate 10,000-HTML-page real HTTP fixture completed in **478.72 seconds** on a 2-CPU runner with about 7.75 GiB RAM. It used injected test-only local DNS resolution, production HTTP acquisition, PostgreSQL scheduling and real result persistence. See [raw measured record](scale-result.json) and https://github.com/warhoundai/HoundCrawler/actions/runs/43692230896 . This is controlled-fixture throughput, not internet-wide performance or an 8-CPU reference result.

No Firecrawl comparison was performed without a dedicated user-owned comparison key. No production parity, SLA or all-web coverage claim is made. Optional parser/cloud acceptance remains separate from the core release.
