# Two-minute test before the bulk description import

## Why

1,243 product descriptions still need rewriting. Through the API that is ~311 calls.
Through Shopify's own CSV import it is one upload. The CSV route is only safe if a
partial import (Handle + Body (HTML), no variant columns) leaves variants alone —
so test it on two products before trusting it with 1,243.

## The test

1. Shopify admin → **Products** → **Import**
2. Upload **`TEST-2-products.csv`**
3. Tick **"Overwrite any current products that have the same handle"**
4. Import

## What must still be true afterwards

Both products have two variants. If the import is safe, all of this is unchanged:

**Mas La Chevalière, Chardonnay IGP Pays d'Oc 70cl** (`chardonnay-white-wine`)

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Single Bottle 70cl | MASLACHEV-CHARDONNAY-70CL | 22.00 | 76 |
| Case of 6 · Save 10% | MASLACHEV-CHARDONNAY-CASE6 | 118.80 | 24 |

**Maison Louis Latour Chardonnay 2019, 75cl** (`grand-ardeche-chardonnay`)

| Variant | SKU | Price | Stock |
|---|---|---|---|
| Single Bottle 75cl | LLATOUR-CHARDONNAY19-75CL | 32.99 | 3976 |
| Case of 6 · Save 10% | LLATOUR-CHARDONNAY19-CASE6 | 178.15 | 24 |

The description should now open with the wine copy rather than `@import url(...)`.

## Then tell me

I will re-query both products and confirm variants, SKUs, prices and stock against the
table above before anything else is imported.

- **Variants intact** → import `ALL-remaining-products.csv` (1,243 products, one upload).
- **Anything changed** → stop. Do not import the large file. I will revert these two from
  the backup and finish through the API instead.

## Note

`ALL-remaining-products.csv` is 9.8 MB. Shopify's import limit is 15 MB, so it fits, but
it may need a few minutes to process.

Originals for all 1,258 products are backed up, so either route is reversible.
