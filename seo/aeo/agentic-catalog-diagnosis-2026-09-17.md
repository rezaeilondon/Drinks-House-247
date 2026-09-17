# "1.21K → 121 products synced" — diagnosis

## First: the catalog is intact

Nothing was mass-unpublished. Counts pulled live on 2026-09-17:

| Measure | Count |
|---|---|
| Products, all statuses | 1,449 |
| Active | 1,257 |
| Active **and** published | 1,242 |
| Active, published **and** in stock | 1,169 |
| Included in Online Store publication | 1,357 |
| Facebook & Instagram / Google & YouTube / Pinterest | 1,311 each |
| Inbox | 1,333 |

**No channel is anywhere near 121.** Every publication holds 1,311–1,357 products. The
old "1.21K" matches the 1,242 active-and-published figure. So whatever is showing 121 is
applying its own filter — it is not reading a shrunken catalog.

## Which surface is it?

Not determinable from the Admin API, because the agentic connectors keep their sync state
internally. They do not appear as publications or catalogs. The installed apps that could
plausibly show a "products synced" figure are:

- **Shopify Perplexity MCP App** (`shopify-perplexity-mcp-app`)
- **Shopify Claude Connector App** (`shopify-claude-mcp-app`)
- **Marketplace Connect** (`shopify-marketplace-connect`)

Also installed and worth knowing about: two apps titled **"javad"** with `null` handles —
custom or unlisted apps with no public identity.

## Two structural defects that would fail almost any agentic eligibility check

These are store-wide and they are the strongest candidates if the surface tightened its
requirements.

### 1. No product carries a GTIN. Zero.

310 active, published products sampled across two different slices of the catalog.
**Every single one has `barcode: null`.**

GTIN — the EAN/UPC on the back of the bottle — is the primary key shopping and agentic
systems use to match a listing to a known product. Every bottle Drinks House 247 sells is
a branded, mass-manufactured item that already has one printed on it.

### 2. The brand field says "Drinks House 247" on 1,253 of 1,257 active products

Shopify's `vendor` maps to `brand` in every feed. It is set to the *retailer* almost
everywhere, not the producer. Only four products name a real brand: Rhum J.M, Clase Azul,
Aberfeldy, R. López de Heredia Viña Tondonia.

Taken together, these two mean an agent cannot establish that this store's "Glenfiddich 12
Year Old" is the same object as anyone else's. There is no GTIN to match on and the brand
reads as a shop, not a distillery. For a price-comparison or personal-shopper agent, an
unmatchable product is an unrecommendable one.

## Three smaller findings

- **`autoPublish` is `false` on all five channels.** Every newly created product must be
  published to each channel by hand, or it silently reaches none of them.
- **26 products are published to no channel at all** (`published_status:unavailable`).
- **73 active, published products are out of stock.** Most agentic and shopping surfaces
  drop out-of-stock items, so these would not sync regardless.

## What to do

1. **Say which app shows the 121** — Perplexity, Claude Connector, or Marketplace Connect.
   The fix depends entirely on which, and each reports its own eligibility errors.
2. **Check that app for a rejected/ineligible list.** A drop this sharp usually comes with
   per-product reasons, which beats inferring from the outside.
3. **Populate barcodes.** The highest-value catalog fix available, and it unlocks
   matching across every agentic and shopping surface at once, not just this one.
4. **Set `vendor` to the actual producer.** Mechanical for most of the catalog since the
   brand is already the first words of the product title.
5. **Turn on `autoPublish`** for the channels that should carry everything.

Items 3 and 4 are worth doing whichever app is at fault. Item 1 should come first, because
a partial sync in progress would explain 121 with nothing wrong at all.
