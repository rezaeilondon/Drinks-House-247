# Full store catalog for LLM and AI crawlers

## What was wrong

`/llms.txt` is the file LLM crawlers fetch to learn what a store sells. Ours
was serving **1,439 bytes** — effectively nothing. At ~600 bytes per product
entry it could not hold more than about two products.

The 158KB, 214-product file in `templates/llms.txt.liquid` was never reaching
anyone. Shopify does not route arbitrary template filenames, which is why Smart
SEO also created a URL redirect from `/llms.txt` to a CDN-hosted text file —
and it was that CDN file, not the template, that was 1.4KB.

Two consequences:

- The store's real catalog was invisible to every AI crawler.
- The redirect pointed at a stale version string (`?v=1784248418`, 2026-07-17)
  even though the file behind it had been updated on 2026-08-30.

Smart SEO's export was also short everywhere else: it listed 42 collections of
214, and 15 pages of 421.

## What replaced it

`build_llms_txt.py` generates the complete catalog from live Admin API data:

| | Smart SEO | Now |
|---|---|---|
| Products | 214 (in an unserved template) | **1,242** |
| Collections | 42 | **207** (non-empty) |
| Pages | 15 | **421** |
| Articles | 27 | **42** |
| Bytes actually served | 1,439 | **739,775** |

`/llms.txt` and `/llms-full.txt` both now redirect to it.

## Regenerating

The file is a snapshot, so prices and stock drift — that is how the previous
one rotted between July and September. To refresh:

1. Re-pull live data into `cat/` (products keyed by gid, plus collections,
   pages and blogs). See the queries in the session notes; each is a paged
   `products(first: 250, query: "status:active")` with variants and price range.
2. `python3 build_llms_txt.py > llms.txt`
3. Validate: every published product present, no duplicates, and **zero matches
   for `@import`, `font-family` or `--ink:`** — CSS leaking into descriptions is
   the exact defect this catalog exists to avoid.
4. `stagedUploadsCreate` (resource FILE, mimeType text/plain, httpMethod PUT) →
   PUT the file → `fileCreate` → poll until `fileStatus` is `READY` → take its
   `url` → `urlRedirectUpdate` both `/llms.txt` and `/llms-full.txt` to it.

## Description text

Descriptions prefer the `lux-lede` / `lux-story` / `dh-lede` paragraphs, which
are the hand-written summary sentences. A flat tag-strip concatenates badge and
spec-table text into run-on fragments, so the class-aware path is used first and
the flat strip is only a fallback.

Where a product appears in `../bulk/rewrite/plan.json.gz`, the cleaned
`descriptionHtml` is used. Its prose is byte-identical to what is live today —
only the `<style>` block's position differs — so the catalog is accurate whether
or not that product's rewrite has been applied yet.

## Crawler access

`templates/robots.txt.liquid` does not exist, so the store serves Shopify's
stock robots.txt. That does not block `GPTBot`, `ClaudeBot`, `PerplexityBot`,
`CCBot` or `Google-Extended`, so no crawler is being turned away.
