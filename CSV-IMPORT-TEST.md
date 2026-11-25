# Bulk description import — what failed, and the two routes left

## What went wrong

The first `TEST-2-products.csv` had two columns, `Handle` and `Body (HTML)`.
Shopify's importer rejected it: **`Title` is required**. Nothing was imported and
nothing in the store changed.

That rejection exposed a wrong assumption. A real Shopify product export is
**78 columns with one row per variant**, not one row per product. The two-column
idea was never going to work, and the three-column version below only fixes
*validation* — it does not answer what the importer does to variants it cannot see.

## Why that matters here

57 of the remaining products carry a second **"Case of 6 · Save 10%"** variant.
A CSV that names no `Option1 Name` / `Option1 Value` / `Variant SKU` / `Variant Price`
columns may leave those variants alone, or may collapse the product to a single
default variant and take the SKUs, prices and stock with it. Untested either way.

## Route A — export first, patch only the description (recommended)

1. Shopify admin → **Products** → **Export** → *All products* → *Plain CSV file*
2. Attach the downloaded file (~6 MB)
3. Only the `Body (HTML)` cell is replaced, per product, matched on `Handle`.
   All 77 other columns and every variant and image row stay byte-identical to
   Shopify's own output.
4. Re-import that file.

No variant risk: every value except the description comes from the store itself.
One export, one import, the whole job done.

**Do not import `products_FINAL_COMPLETE.csv`** (14 September, in this repo). It
predates the 108 meta descriptions, the 49 SEO titles, the brand backfill, the
collection work and the 24 descriptions fixed on 18 September. Importing it would
roll all of that back. The export has to be fresh.

## Route B — the three-column test, on two products

`TEST-2-products.csv` now carries `Handle`, `Title`, `Body (HTML)` and will validate.
Import it with **"Overwrite any current products that have the same handle"** ticked.

Recorded live state, 2026-09-18, to check against afterwards:

**Mas La Chevalière, Chardonnay IGP Pays d'Oc 70cl** — `chardonnay-white-wine`

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Single Bottle 70cl | MASLACHEV-CHARDONNAY-70CL | 22.00 | 76 |
| Case of 6 · Save 10% | MASLACHEV-CHARDONNAY-CASE6 | 118.80 | 24 |

Total inventory **100** · SEO title `Mas La Chevalière Chardonnay Pays d'Oc | Wine Delivery UK`
· SEO description **already empty before import** — an empty value afterwards is not damage.

**Maison Louis Latour Chardonnay 2019, 75cl** — `grand-ardeche-chardonnay`

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Single Bottle 75cl | LLATOUR-CHARDONNAY19-75CL | 32.99 | 3976 |
| Case of 6 · Save 10% | LLATOUR-CHARDONNAY19-CASE6 | 178.15 | 24 |

Total inventory **4000** · SEO title `Maison Louis Latour Chardonnay 2019, 75cl - Burgundy Wine`
· SEO description present.

Both variant sets are recorded here precisely so they can be rebuilt through the API
if the import damages them. The blast radius is two products.

## Route C — no CSV

Resume the API route at product 25 of 1,248. Proven, idempotent, reversible, and
already 24 products in with zero errors. Roughly 245 more round trips.

## Current state

24 of 1,248 descriptions fixed via API (`seo/aeo/bulk/description-fix-progress.json`).
The API run is paused so it cannot collide with an import. Originals for all 1,258
products are backed up, so every route is reversible.
