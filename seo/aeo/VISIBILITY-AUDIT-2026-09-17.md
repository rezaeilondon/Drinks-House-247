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

---

## Draft theme: `SEO fix - remove duplicate product schema (review 1st)`

Theme id `193644724599`, duplicated from the live theme on 2026-09-17. **Unpublished.**
Publishing is blocked by the same safety policy, so it is a manual step in Shopify admin.

### Correction to the API note above

The earlier claim that "theme writes are blocked" was too broad, and so was the
correction to it. The precise rule, from the connector itself: **theme file writes are
allowed on unpublished themes only; writes targeting the live/MAIN theme are blocked.**
`themeFilesDelete` and `themePublish` are blocked outright. That is why the work lands on
a draft and why publishing is yours.

### What changed

| File | Change |
|---|---|
| `snippets/dh247-clean-description.liquid` | New. Sets `dh_clean_description` = `product.description` with hand-written Product JSON-LD removed. |
| `sections/product-template.liquid` | 5 lines. Includes the snippet, and points the 4 description outputs at `dh_clean_description`. |
| `snippets/dh247-legal.liquid` | New. Companies Act 2006 s.82 trading disclosure. |
| `sections/footer.liquid` | 5 lines. Includes the legal snippet after the copyright line. |

Both edited files were diffed against the live originals after writing: the diffs contain
the intended changes and nothing else.

### Why a snippet rather than an edit per product

`productUpdate` replaces `descriptionHtml` wholesale and `bulkOperationRunMutation` is
blocked, so 1,246 individual rewrites were not viable. Stripping at render time fixes
every product page in one change. `include` is used rather than `render` because `render`
runs in an isolated scope and the assign would not reach the caller.

The strip was verified against all 1,246 affected descriptions before deployment:
output identical to the reference Python strip, zero Product schema surviving, zero
content loss on a 400-product sample.

**This is a render-time fix.** The stale blocks remain in the product records, so a CSV
export or another app could still surface them. The permanent fix is still the bulk strip.

### Also corrected: the CSS extraction idea was wrong

An earlier suggestion to extract the inline `<style>` blocks into a stylesheet was
dropped after measuring it. There are 49 distinct blocks and 4.10 MB of inline CSS across
the catalogue, but **no visitor downloads that** — it is **3.3 KB per product page**,
about 1.7% of page weight. Moving it to an external stylesheet would add a render-blocking
request on first visit, which is worse for exactly the first-time organic visitor that
SEO cares about. Inlining critical CSS is the recommended practice. Not an SEO lever.

### Content quality, measured

Worth recording because it changes what is worth doing next: **91% of the visible text on
product pages is unique to that product**, only 8% is boilerplate, and exactly **1**
product has under 400 characters of unique text. Content depth is not the problem.
1,247 of 1,257 products already carry a rich template.

### Still yours to do

1. **Preview the draft, then publish it.** Check a product page with a big description
   (Pallini Limoncello, any hamper) and one without (`Untitled Jun7_17:13:07`).
2. **Verify VAT `GB 339765749`** at gov.uk "Check a UK VAT number" before publishing.
   If it fails, delete the VAT sentence from `snippets/dh247-legal.liquid`.
3. **Shop name is `"Drinks House 247 "`** — trailing space. There is no `shopUpdate`
   mutation in the Admin API, so this is admin-only.
4. **`billingAddress.city` is `"Battersea, london"`** — malformed. Admin-only, same reason.
   Fix it, then turn on `EnableStoreAddress` and `EnableStructuredDataForRealStore`
   in Smart SEO to emit LocalBusiness data.
5. **Delete `assets/dh247-write-probe.css`** from the unpublished theme "Copy of Copy of
   Copy of Copy of New - RE | GSC...". It is 34 bytes, unreferenced, and inert;
   `themeFilesDelete` is blocked so it could not be removed here.
6. **The Prestige Pearl gift set** shows **£390** on 47 other product pages but sells for
   **£380**. Decide which is right — that is a pricing call, not a fix.

---

## Are product pages at their optimum? No. Measured 2026-09-17.

### First, a methodology correction

An initial pass audited Shopify's native `seo.title` / `seo.description` fields and
reported 573 over-long meta descriptions and 372 over-long titles. **Those numbers were
measuring the wrong fields.** `snippets/smartseo.product.metatags.liquid` overrides both
at render time whenever a Smart SEO template is active, and one always is:

- A **shop-wide bulk template** exists in `shop.metafields['product-bulk']['seo-template']`,
  set 2020-05-26: `${title} | 30 Min | Alcohol Delivery London` for the title and
  `${default-meta-description}` for the description.
- **376 active products** additionally carry their own
  `product.metafields['product_seo']['seo_tags']`. The snippet picks whichever template
  has the highest timestamp, and per-product ones (2021) beat the bulk one (2020).

So the native fields are only reached through `${default-meta-*}` substitution. The
figures below are what the page actually renders, applying Smart SEO's own precedence and
its 300-character description truncation.

(`metafields.product_seo.seo_tags:*` is another filter Shopify accepts and ignores —
it returns all 1,449, as does a nonsense key. The metafield had to be fetched per product.)

### What renders today

| | Active products |
|---|---|
| Using a per-product Smart SEO template | 376 |
| Falling back to the shop-wide bulk template | 882 |
| **Rendered `<title>` longer than 60 chars** | **671 (53%)** |
| **Rendered meta description longer than 160** | **393 (31%)** |
| **Rendered meta description empty** | **108 (9%)** |
| At least one rendered defect | **794 of 1,258 (63%)** |

Rendered title: median 62 characters, longest 147. Meta description: median 149, capped
at 300 by the app.

### The single biggest cause is one setting

The bulk template appends ` | 30 Min | Alcohol Delivery London` — 34 characters — to every
product title it touches. Product titles here average around 40 characters, so the result
lands near 74 and Google truncates it. **Editing that one template fixes most of the 671.**
It is also the same boilerplate on 882 titles, which wastes the most weighted text on the
page repeating a phrase the site already ranks for.

### Honest weighting

Title and description length are **not ranking penalties**. An over-long title is
truncated in the result, and meta description is not a ranking factor at all — both cost
click-through, not position. They are worth fixing because they are cheap, not because
they are severe.

These are more concrete:

| Defect | Count | Why it matters |
|---|---|---|
| Handle still `untitled-*` on a real product | 7 | The URL is a permanent, visible ranking and trust signal |
| Title in ALL CAPS | 22 | e.g. `LAPHROAIG OAK SELECT 70cl`, `AMIE ROSÉ 75CL` |
| Featured image with no alt text | 56 | Image search, and accessibility |
| Active but not on the online store | 15 | No public URL at all |

The seven junk URLs are real products: Laphroaig 10 Cask Strength, Laphroaig Oak Select,
The Celebration Hamper, Jack Daniel's Family Miniature Gift Set, two Seventy One Gin sets,
and Amié Rosé. Changing a handle needs a 301 from the old one, so it is a deliberate job,
not a bulk edit.

Eight further products are literally titled `Untitled Jan21_21:54` and similar. All eight
are **DRAFT**, so they are not indexed — clutter rather than a live defect.

### What is already right

Worth stating so effort goes to the right place: duplicate metadata is nearly absent
(2 repeated titles, 4 repeated descriptions across 1,258 products), every active product
has a product type, and 91% of on-page text is unique per product. The content is good.
The metadata wrapper around it is what is not.

### Order of work, by value per unit of effort

1. Rewrite the bulk SEO template so titles fit — one edit, ~671 titles.
2. Fill the 108 empty meta descriptions.
3. Fix the 7 `untitled-*` handles with 301 redirects.
4. Title-case the 22 shouting titles; add alt text to 56 images.

---

## Fixes applied live, 2026-09-17

All pushed to the live store and read back afterwards.

### 1. The bulk SEO title template — ~365 pages

`shop.metafields['product-bulk']['seo-template']` changed from
`${title} | 30 Min | Alcohol Delivery London` to `${title} | Drinks House 247`.

The old suffix was 34 characters, which left **668 of 882** bulk-driven titles over
Google's ~60-character display limit. The new one is 19, leaving 303. Measured before
choosing:

| Suffix | Titles still over 60 |
|---|---|
| `\| 30 Min \| Alcohol Delivery London` (old) | 668 of 882 (76%) |
| `\| Drinks House 247` (chosen) | 303 (34%) |
| none at all | 72 (8%) |

Dropping the suffix entirely would fix more, but every result loses the brand name, so
the conventional option was taken. Reversible with one metafield write.

**The timestamp was deliberately left unchanged** at `15905089034551011`. Smart SEO
resolves competing templates by highest timestamp, so raising it would have made the bulk
template override the 376 per-product templates from 2021. Keeping it identical changes
only the wording.

### 2. ALL-CAPS titles — 47, not 22

The first scan used `len(title) > 8 and title == title.upper()`, which missed `GUINNESS`
(exactly 8 characters), `HARIBO`, and anything with a lowercase unit like
`LUC BELAIRE LUXE RARE 75cl`. A word-level scan found 25 more. Fixed in two passes:
Gosset ×7, Ayala ×3, Van Wees ×5, Bonpland ×2, Procera ×2, Cotswolds ×2, Diplomático ×2,
Luc Belaire ×3, and singles including Guinness, Haribo, Nurofen, Rampur, Michel Couvreur,
Bernard-Massard, Tarlant, Amour de Deutz, Dom Pérignon Basquiat, Compass Box Brûlée Royale.

Deliberately **not** changed, because the capitals are the real brand styling:
`LOUIS XIII`, `NEFT`, and the abbreviations `V.S`, `X.O`, `L.B.V`, `D.O.M.`, `NV`, `VORS`.

### 3. Image alt text — 55 products

Set from each product's own title, which is accurate and descriptive rather than invented.
The 56th, "Service Fee", has no image at all.

### 4. The seven `untitled-*` URLs

Renamed, each with a 301 redirect from the old path so nothing 404s:

| Was | Now |
|---|---|
| `/products/untitled-feb8_03-31` | `/products/amie-rose-75cl` |
| `/products/untitled-may29_15-51` | `/products/laphroaig-10-year-old-cask-strength-70cl` |
| `/products/untitled-may29_16-53` | `/products/laphroaig-oak-select-70cl` |
| `/products/untitled-jun7_02-52-44` | `/products/the-celebration-hamper` |
| `/products/untitled-jun11_15-11-04` | `/products/jack-daniels-family-miniature-gift-set-3x5cl` |
| `/products/untitled-jun13_02-01-56` | `/products/seventy-one-gin-trudon-candle-luxury-gift-set` |
| `/products/untitled-jun13_03-01-29` | `/products/seventy-one-gin-signature-martini-gift-set` |

Verified: `productsCount(query: "status:active AND handle:untitled*")` now returns **0**,
with a nonsense-prefix control also returning 0, so the filter is real.

### Still open

- **108 products render no meta description.** Writing these needs product knowledge per
  item; they are listed in `bulk/product-page-seo-defects.csv`.
- **303 titles still over 60 characters**, because the product titles themselves are long
  (longest: 112 characters). No template can fix that — it needs editing the titles.
- **393 meta descriptions over 160 characters.** Smart SEO already caps them at 300.

---

## GTIN experiment — running log

Testing whether a GTIN is what gates acceptance into the Microsoft Copilot channel.
Shopify stores no per-product feedback, so a controlled before/after count is the only
way to find out.

**Baseline: 124 synced, 2026-09-17.** Background churn is roughly ±3 — the count moved
121 → 124 with no GTIN change at all, so a handful of products cannot be distinguished
from noise. The batch needs to be nearer 30 before a result means anything.

### Validation rule for every barcode

Two checks before anything goes live, because a wrong GTIN binds the product to another
company's catalogue entry and is worse than an empty field:

1. **Mod-10 check digit** must pass (GS1 standard, alternating 3/1 weighting from the
   right).
2. **GS1 country prefix must be consistent with the producer.** This is the check that
   actually catches bad data — a made-up number can still pass its checksum.

### Log

| Product | Barcode | Checksum | Prefix | Outcome |
|---|---|---|---|---|
| Dom Pérignon P2 2003 75cl | `3185370699058` | pass | 318 → France | live |
| Cazcanes No.7 Añejo 75cl | `7500462805432` | pass | 750 → Mexico | live |
| Clase Azul Reposado 70cl | `1230000130011` | pass | **123 → USA/Canada** | **cleared** |

The Clase Azul code passed its check digit but its prefix is a US/Canada range, while
Clase Azul is distilled in Jesús María, Mexico — its EAN should begin `750`, as the
Cazcanes one does. The digit pattern (`123-0000-13001-1`) also has the shape of an
internal or placeholder code rather than a GS1-issued one. Cleared to null on the owner's
instruction, pending a reading from the physical bottle.

This is the case for validating prefixes rather than checksums alone: the checksum passed.

**Count so far: 2 of a target 30.** Candidate list with variant IDs is in
`bulk/gtin-test-batch.csv`.
