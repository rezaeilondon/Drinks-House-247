# Two-minute test before the bulk description import

24 of 1,248 products are already fixed through the API. The CSV route covers the
remaining 1,224 in one upload — but only if a partial import leaves everything
except the description alone. Test that on two products first.

## The test

1. Shopify admin → **Products** → **Import**
2. Upload **`TEST-2-products.csv`** (2 products)
3. Tick **"Overwrite any current products that have the same handle"**
4. Import

## Recorded state, immediately before import (2026-09-18)

These are the values I will check against. Nothing here should change.

**Mas La Chevalière, Chardonnay IGP Pays d'Oc 70cl** — `chardonnay-white-wine`

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Single Bottle 70cl | MASLACHEV-CHARDONNAY-70CL | 22.00 | 76 |
| Case of 6 · Save 10% | MASLACHEV-CHARDONNAY-CASE6 | 118.80 | 24 |

- Total inventory: **100**
- SEO title: `Mas La Chevalière Chardonnay Pays d'Oc | Wine Delivery UK`
- SEO description: **empty** (already empty before the import — not caused by it)

**Maison Louis Latour Chardonnay 2019, 75cl** — `grand-ardeche-chardonnay`

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Single Bottle 75cl | LLATOUR-CHARDONNAY19-75CL | 32.99 | 3976 |
| Case of 6 · Save 10% | LLATOUR-CHARDONNAY19-CASE6 | 178.15 | 24 |

- Total inventory: **4000**
- SEO title: `Maison Louis Latour Chardonnay 2019, 75cl - Burgundy Wine`
- SEO description: `Maison Louis Latour Chardonnay 2019, 75cl, offers a classic Burgundian taste
  with notes of green apple and citrus. Perfect pairing for seafood or creamy pasta.`

## What should change

Only the description. Both should stop opening with `@import url(...)` and start
with the wine copy instead. The styling on the page should look identical.

## Then tell me

I re-query both products and check all four variants, both SKUs, prices, stock,
totals and SEO fields against the table above.

- **Everything matches** → import `ALL-remaining-products.csv` (1,222 products, 9.7 MB,
  one upload) and the whole job is done.
- **Anything differs** → stop. Do not import the large file. I revert these two from
  the backup and finish the remaining 1,224 through the API instead.

Originals for all 1,258 products are backed up either way, so nothing here is one-way.
