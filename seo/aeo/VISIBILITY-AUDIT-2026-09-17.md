# Visibility audit — Google and LLM retrieval

Read back from the live Admin API on 2026-09-17. Every count below was measured,
not estimated, and each filter was validated with a control query first — Shopify
silently ignores several filter keys and returns the whole catalogue, so an
unvalidated count is worthless.

## Filters that silently lie

`productVariantsCount(query: "barcode:*")` returns 1,546 — the entire variant
count. So does `-barcode:*`, and so does a nonsense value. The same is true of
`has_image:`. These keys are accepted and ignored. Any figure taken from them is
meaningless. Where a filter mattered, it was proved with a control:
`published_status:999999999-published` returns 0, so channel filters are real.

## The duplicate Product schema

**1,246 of 1,257 active products carry a hand-written `Product` JSON-LD block
inside the description HTML.** The theme also emits one per request:
`layout/theme.liquid` includes `snippets/smartseo.liquid`, which renders
`smartseo.product.jsonld` whenever
`shop.metafields['smartseo-settings']['json-ld'].EnableStructuredData` is true.
It is true. So every one of those product pages publishes **two competing Product
entities**, and the hand-written one is frozen at the moment it was written while
the app's is generated live per variant.

That was verified before touching anything. Stripping a page's schema when no
replacement existed would have been worse than leaving it.

### What has already drifted

| Defect | Count | Evidence |
|---|---|---|
| Hard-coded price no longer matches the live price | **18** | `bulk/jsonld-price-drift.csv` |
| Declares `InStock` while genuinely unpurchasable | **4** | see below |
| Cross-sell card price no longer matches target | **47 labels, 1 product** | `bulk/crosssell-price-drift.csv` |

Worst price drift: The Malt Collector's Hamper advertises **£375** in schema and
sells for **£290**. The Murakami Prestige Hamper: **£695** against **£620**.
Don Julio 1942: **£225** against **£165**.

### Availability: a correction worth recording

An initial pass flagged 12 products as declaring `InStock` with zero stock. That
was **wrong**, and the error is instructive: `totalInventory: 0` does not mean
unavailable. Where `inventoryItem.tracked` is false, Shopify reports zero while
the product still sells normally. The correct test is `variants.availableForSale`.

Re-tested on that basis, only **4** products genuinely misdeclare availability:

- Rhum J.M VSOP Rhum Agricole Vieux 70cl
- Indri Diwali Collector's Edition Indian Single Malt Whisky 70cl
- López de Heredia Viña Tondonia Tinto Reserva 2011 — 75cl *(fixed)*
- López de Heredia Viña Tondonia Tinto Reserva 2011 — 150cl Magnum *(fixed)*

The other eight — Michter's, Christian Drouin, Barsol, Kavalan, Yatir Forest,
Strongbow, Guinness, Stella Artois — have inventory tracking switched off and are
genuinely for sale. Their `InStock` is accurate.

## Why this matters more for Google than it looks

The Google & YouTube channel feeds Merchant Center through the publication API,
not by scraping the page, so a wrong price in page schema does not by itself
break the feed. It breaks the *reconciliation*: Google crawls the landing page to
verify the feed, and a second Product entity carrying a different price is what
triggers price-mismatch item disapprovals. For an LLM reading the page there is
no reconciliation at all — it simply reads a wrong number.

## The fix, and why it is not finished

Deleting the hand-written block is the correct fix rather than correcting its
numbers, which would only reset the clock until the next price change.
`strip_product_jsonld.py` removes a block only when it parses as JSON **and**
declares `"@type": "Product"`; anything unparseable or of another type is left
untouched. Across all 1,257 products it removes 1,246 blocks and keeps 0 others,
and a byte-level diff on a sample shows the delta is exactly the script block.

**Two products are fixed** (the two López wines, which were the acute
availability cases). **1,244 remain.**

The blocker is mechanical, not technical. `productUpdate` replaces
`descriptionHtml` wholesale, and these descriptions average ~20KB — some are
39KB. Pushing 1,244 of them one mutation at a time is not viable.
`bulkOperationRunMutation` is the right tool and the payload was built and
uploaded successfully (10.4MB JSONL, staged upload returned 201), but the bulk
mutation itself is **blocked by this session's MCP safety policy**, on the
grounds that it can run arbitrary mutations. That restriction was not worked
around.

Completing it needs one of:

1. Running the prepared JSONL through `bulkOperationRunMutation` from a context
   where it is permitted.
2. A CSV/description import app (Matrixify or similar).
3. Regenerating the descriptions from source without the block.

`bulk/products-strip-product-jsonld.csv` lists all 1,246 affected products.

## Other live defects found

- **Shop name is `"Drinks House 247 "`** — trailing space. It propagates into
  structured data and page titles.
- **`billingAddress.city` is `"Battersea, london"`** — two locality values in one
  field, lowercase second. This is why `EnableStoreAddress` and
  `EnableStructuredDataForRealStore` are both still false in the Smart SEO
  settings: turning them on would publish a malformed address. Fix the address
  first, then enable both — that is what emits LocalBusiness data for local search.
- **`autoPublish` is false on all five publications**, including Online Store and
  Google & YouTube, so new products reach no channel until published by hand.
  Deliberately left alone: the owner declined publishing the currently hidden
  products, which suggests manual control is intended.
- **220 product descriptions assert "4.8 on Google · 223 reviews"** and link
  Trustpilot. Not verified here; if the figure has moved, it is wrong in 220
  places at once and should be sourced from a review app rather than hard-coded.
- **1,449 products, 1,546 variants, zero GTINs.** Unchanged, and still the single
  biggest constraint on shopping and agentic surfaces.
