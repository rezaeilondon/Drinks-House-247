# Bulk remediation set

Generated 2026-09-15 from a full pull of every article, product and page in the store.
Each CSV holds the **already-corrected body** for every resource that still needs the
internal-link fix, so no transformation has to be re-derived.

| File | Rows | Absolute links fixed | `target=_blank` stripped | `www` → apex |
|---|---|---|---|---|
| `pages-fixed.csv` | 366 | 5,467 | 146 | 514 |
| `products-fixed.csv` | 211 | 1,857 | 81 | 0 |
| `articles-fixed.csv` | 196 | 886 | 294 | 87 |

Columns: `ID` (numeric Shopify id), `Handle`, `Command` (always `UPDATE`), `Body HTML`.

## Why a CSV and not an API run

`bulkOperationRunMutation` is blocked by the MCP safety policy (re-tested 2026-09-15:
*"Bulk mutation operations are blocked — they can execute arbitrary mutations"*).
Writing 773 resources one at a time through the Admin API is possible but slow and
expensive, so the corrected bodies are shipped here instead. Import them with a
bulk-import app (Matrixify and similar accept this column layout) or feed the CSV to a
script holding an Admin API token.

**Re-generate before importing if the store has been edited since 2026-09-15** — these
bodies are a snapshot. `fix_links.py` is idempotent, so re-running it on a fresh pull is
safe and is the correct way to refresh the set.

## What the transformation does

See `../fix_links.py`. Four content-preserving changes, applied only to **internal**
links:

1. `href="https://www.drinkshouse247.co.uk/x"` → `href="/x"` — an absolute URL throws an
   `/ar`, `/ru` or `/zh` reader back into English mid-journey.
2. A bare-domain href → `/`.
3. `target="_blank"` / `target="_new"` (and the companion `rel`) removed from internal
   links only. External links — Google reviews, Trustpilot, Drinkaware — keep both.
4. Any remaining `www` host → the apex `https://drinkshouse247.co.uk`, including a
   scheme-less mention in prose. These are JSON-LD values that must stay absolute.

External links are never touched.
