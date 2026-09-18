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

---

## Collections: content written for 8 pages, 2026-09-17

Collections had not been audited before this. They turned out to be in far better shape
than products: **no empty collections, none with fewer than 4 products**, 91% carry a body
description, 92% an SEO title. There is no shop-wide Smart SEO template for collections,
so the native fields are what render.

The exception was a cluster of pages that were completely blank — no SEO title, no meta
description, and no body content at all — despite holding hundreds of products between
them:

| Collection | Products | Was |
|---|---|---|
| `wines-that-pair-with-salmon` | 186 | nothing |
| `wines-that-pair-with-chicken` | 184 | nothing |
| `wines-that-pair-with-risotto` | 167 | nothing |
| `wines-that-pair-with-oyster` | 65 | nothing |
| `wines-that-pair-with-shellfish` | 65 | nothing |
| `wines-that-pair-with-pasta` | 56 | nothing |
| `shop-by-case` | 25 | nothing |
| `tennessee-whisky` | 4 | nothing |

These are informational-intent pages — "what wine goes with salmon" is a question people
actually type — attached to real inventory. Blank, they could match nothing.

All eight now have an SEO title under 60 characters, a meta description under 160, and a
body of genuine pairing guidance organised by preparation or sauce rather than by grape,
because that is how someone actually arrives at the question. Each ends with internal
links into the relevant product collections; all eleven link targets were verified to
resolve before publishing.

The content is standard oenological guidance — Chablis with oysters rests on the
Kimmeridgian limestone the vines grow on, the Lincoln County Process is what legally
separates Tennessee whiskey from bourbon. Nothing is claimed about stock levels, awards or
customer numbers.

### Remaining collection work

- **30 of 100 collection SEO titles exceed 60 characters** and will truncate in results.
- **9 meta descriptions exceed 160 characters.**
- **84 of 100 collections have no image**, which costs nothing in ranking but affects how
  the page looks when shared.

---

## Internal linking and blog audit, 2026-09-18

### The premise needed correcting first

The brief was to make sure every collection has internal inbound links from articles,
pages or products. Measured across **214 collections, 272 articles, 421 pages and 1,257
products**, that foundation already existed:

| | Before |
|---|---|
| Internal links pointing at collections | **6,092** |
| Collections with zero inbound links | 8 |
| Collections with 1–2 | 77 |
| Collections with 3+ | 129 |
| Published articles linking to a collection | **257 of 259** |

Articles were not the weak point either: median body length **8,328 characters**, only 2
under 600, and only 3 with no internal link at all.

**Six of the eight orphans have no products.** Linking to an empty collection page is
worse than leaving it orphaned, so the fix there is not a link.

### What was actually done

Built two topic clusters, where each page links to its siblings:

| Cluster | Pages | Inbound links each, before → after |
|---|---|---|
| Wine pairing guides | 12 | 2 → **13** |
| Gift price bands | 6 | 2 → **7** |

Re-measured from the live store afterwards:

| | Before | After |
|---|---|---|
| Links into collections | 6,092 | **6,223** (+131) |
| Weak (1–2 inbound) | 77 | **59** |
| Healthy (3+ inbound) | 129 | **147** |

Also written from scratch: a body for `wines-that-pair-with-seafood-1`, which had none.
All 28 distinct link targets were verified to resolve before publishing; zero broken.

The three articles with no internal links now have contextual collection links:
corporate gifting → corporate gifts and budget bands, wine racks → reds, whites and
cases, London celebrations → champagne, spirits and hampers.

### The more serious finding: unmarked sponsored links

While reading the articles, a scan of all outbound links found **185 external links, 72
of them dofollow**. Most are legitimate citation (NHS, Drinkaware, NCBI, trade press) and
should stay that way. But a blog literally named **"Sponsored"** was passing dofollow
links to its advertisers.

Google's link spam policy requires paid or sponsored links to carry `rel="sponsored"` (or
`nofollow`). Passing ranking signal to advertisers without it is a link scheme, and it
risks a manual action against the site.

Fixed immediately — four advertiser links now carry `rel="sponsored nofollow"`:

| Article | Link |
|---|---|
| Beautiful Wine Rack Ideas | `winecellarhq.com` ×3 |
| A Traveler's Guide to Celebrating in London | `radicalstorage.com` |

Academic citations in those same articles were left dofollow, because they are genuine
references rather than paid placements.

### Still to review — `bulk/external-dofollow-review.csv`

These are dofollow links to commercial domains that need a human judgement on whether
they were paid, exchanged, or genuinely editorial. Two stand out:

- **`luxuryspirits.com` and `corporategiftshampers.co.uk`** — these look like direct
  competitors receiving ranking signal from a gift-hamper article.
- **`rankpill.com` ×2** — an SEO content generator credit, on two articles.
- **`drinks-house.co.uk` ×4** — a separate domain linked from one article.
- Unrelated commercial domains in a drinks blog: `builderdepot.co.uk`, `diy.com`,
  `discountcream.co.uk`, `li.me`, `winedom.co.uk` (in the privacy policy).

The restaurant links on `/pages/red-wine-delivery` were left alone — a London drinks
retailer citing London restaurants reads as editorial.

### Empty collections — recommend hiding, not linking

Seven collections show zero products. Their rules are correct; there is simply no stock.
Verified with a control query that the title filter works: the catalogue contains no
Viognier, no Torrontés, and nothing tagged Sardinia, sparkling red, carbon neutral,
biodynamic or Doux.

These are thin-content pages. They should be unpublished from the Online Store until
stocked, then republished. Not done unilaterally — hiding live pages is the owner's call.

---

## 2026-09-18 — Site-wide broken internal link & redirect audit

First full crawl-graph check of the store. Built the complete live URL inventory
(214 collections, 1,449 products, 421 pages, 272 articles) and resolved **every
internal link** in every collection description, article body, page body and
product description against it.

**11,228 internal links checked → 358 pointed at URLs that do not exist**
(64 distinct targets), concentrated in a few repeated mistakes:

| Broken target | Links | Cause |
|---|---|---|
| `/collections/champagne/products/dom-perignon-champagne` | 65 | product renamed to `-2013` |
| `/pages/delivery-info` | 32 | page removed |
| `/products/charbonnel-et-walker-union-jack-...-truffle-205g` | 30 | handle missing the word `selection` |
| `/collections/champagne/products/veuve-clicquot-vintage-champagne-2012` | 25 | product renamed to `-2015` |
| `/pages/champagne-gift-delivered` | 19 | page consolidated |

### The larger finding: 49 redirects that dead-ended

A cluster of ~49 redirects pointed at **bare root paths** — `/champagne-delivery-london`,
`/24-hour-alcohol-delivery-london`, `/top-off-licenses-near-you-that-deliver` and seven
others. Every one of those is a blog article living at `/blogs/posts/<handle>`. Shopify
does not route bare root paths, so all 49 redirects sent visitors and crawlers to a 404.

Alongside that, three further defect classes:

- **Soft 404s** — 7 redirects whose target was `/`. Google treats redirect-to-homepage
  as a soft 404 and discards the link equity entirely.
- **Lost product intent** — 20 redirects for discontinued vintages pointed at a *collection*
  when the replacement product exists (16 of them for Caymus 2020, whose 2022 is in stock).
- **Redirect chains** — 24 two- and three-hop chains, e.g.
  `/products/hennessy-fine-de-cognac` → `/whisky-cognac` → `/collections/whisky-cognac` → `/collections/whisky`.

### Applied live (92 operations, all re-queried and verified)

| Action | Count |
|---|---|
| Redirects created for hard 404s | 17 |
| Dead-end root-path redirects repointed to `/blogs/posts/…` | 49 |
| Soft 404s (`→ /`) repointed to the right product | 7 |
| Collection-dump redirects repointed to the live product | 20 |
| Redirect chains flattened to a single hop | 24 |

All 358 broken internal links now resolve in one hop. Verified by re-querying the
live store, not by trusting `userErrors: []`.

### Method note — two filters that lie

- `urlRedirects(query:"path:*term*")` returns **zero** for everything; the `*wildcard*`
  syntax is silently unsupported. Bare terms work and match **both** `path` and `target`.
  Confirmed genuine with a nonsense control (`zzqqxx-not-a-real-path` → 0).
- Redirect paths are **case-insensitive**. `/collections/Champagne` and the capital-B
  `Bollinger` link were flagged by the case-sensitive scanner but were never actually
  broken — two false positives out of 64.

### Deferred: `seo/aeo/bulk/internal-link-rewrites.csv`

358 rows / 214 resources, each giving `current_href` → `should_be`. The redirects above
already make every one of these resolve, so this is now an **optimisation, not a fix** —
rewriting the hrefs removes the redirect hop and the crawl-budget cost. Not applied in
session: it needs ~2.8 MB of HTML bodies pushed through the API, which is better done as
a bulk import than interactively.

---

## 2026-09-18 — Pre-publish gate on draft theme 193644724599

**VAT number removed.** `GB 339765749` was never verified, so it is no longer rendered.
Companies Act 2006 s.82 does not require a VAT number, and one that fails a public
gov.uk lookup casts doubt on the entire disclosure — so omitting it is strictly safer
than shipping it unverified. Applied to `snippets/dh247-legal.liquid` on the draft and
mirrored in `seo/trust/footer-legal-snippet.html`. Both carry the exact line to append
once it validates. Company number `11286226`, registered office and premises licence
`2022/320845` all remain — those are the s.82 requirements.

### Drift check — nothing on the live theme would be reverted

MAIN `193478492535` last updated **2026-09-15**; the draft was snapshotted **2026-09-17**.
Confirmed by checksum rather than timestamp alone:

| File | Live | Draft |
|---|---|---|
| `config/settings_data.json` | `fa53b34…` | identical |
| `layout/theme.liquid` | `eac087f…` | identical |
| `snippets/smartseo.product.jsonld.liquid` | `e7a0164…` | identical |
| `sections/product-template.liquid` | 28,590 b | 28,839 b |
| `sections/footer.liquid` | 13,023 b | 13,269 b |

`settings_data.json` is what apps and the theme editor rewrite constantly; byte-identical
means no drift. `layout/theme.liquid` identical means the analytics fix the live theme was
published for survives.

### Liquid verified by reading the template, not from memory

- `{% include 'dh247-clean-description' %}` sits at the **top of the file**, before every
  use — so `dh_clean_description` can never render empty.
- All **three** live description outputs go through `dh_clean_description`. The remaining
  `product.description` references are `!= blank` guards (correct — they test the raw
  source) plus one output inside a `{%comment%}` block that never renders.
- `include` not `render`, deliberately: `render` would not leak the assign into caller scope.

### Incidental finding — orphaned microdata

`sections/product-template.liquid` carries `itemprop` attributes (`name`, `brand`, `sku`,
`price`, `availability`, `description`) but the enclosing `itemscope` was previously
commented out, so they have **no parent item**. Google ignores orphaned `itemprop`, so this
is dead weight rather than a defect — and it usefully confirms that after publishing,
Smart SEO's block will be the *only* Product structured data on the page. No third source
competing.

Footer links verified live and published: `/pages/challenge-25`,
`/pages/authenticity-and-sourcing`, `/pages/reviews`, `/pages/contact-us`
(control query for a nonsense handle returned 0, so the filter is genuine).

### PUBLISHED 2026-09-18T00:46Z

Theme `193644724599` ("SEO fix - remove duplicate product schema") is now **MAIN**.
Old theme `193478492535` ("ANALYTICS FIX") is now **UNPUBLISHED** and remains available
as a one-click rollback. Verified via the themes API.

**Live render NOT verified from this environment.** The egress proxy denies
`www.drinkshouse247.co.uk:443` by policy — `403` on CONNECT via curl, `EGRESS_BLOCKED`
via WebFetch. No workaround attempted. So the following are confirmed only at the
theme-file level, not as rendered HTML:

- one `Product` JSON-LD block per product page instead of two
- footer legal disclosure rendering without a VAT line
- product descriptions rendering non-empty through `dh_clean_description`

These need a human eye on the live site, or Google's Rich Results Test, to close out.
Everything checkable via the Admin API was checked and passed before publish.

---

## 2026-09-18 — 108 products with no rendered meta description: fixed

### Where the fix had to go

Read `snippets/smartseo.product.metatags.liquid` rather than guessing. Smart SEO picks one
template by **highest timestamp** across per-product → vendor → collection → tag → bulk, then
substitutes variables and splits on `:||:` to get title and description.

The shop's bulk template is:

```
${title} | Drinks House 247:||:${default-meta-description}:||:=||=15905089034551011
```

`${default-meta-description}` resolves to `page_description` — i.e. the product's **native**
Shopify SEO description. Timestamps measured live: per-product templates are ~`1.624e16`, the
bulk template `1.5905e16`, so **per-product wins where it exists** (376 products) and the other
882 fall to bulk.

All 108 failing products had **no per-product template**, so they fell to bulk, whose description
slot is the native field — which was empty. Diagnosis: `108 of 108`, not a mix of causes.

**So the fix is the native `seo.description` field**, not a metafield hack. It also survives
Smart SEO ever being uninstalled. One collection-level template exists (a cigarette collection)
but its description slot is also `${default-meta-description}`, so the same fix covers it.

Note: 94 of the 108 also have an empty native `seo.title`. That does **not** matter — the bulk
template's title slot is `${title}`, which is `product.title`, not the SEO field. Titles render.

### The canary that saved 14 SEO titles

Before batching, one product was updated with `seo:{description: …}` alone. Read-back showed
`seo.title` had gone from `"Patron XO Cafe Tequila - 24 Hour Alcohol Delivery London"` to
**`null`**. A partial `seo` input on `productUpdate` **clobbers the omitted field**. Batching
all 108 blind would have destroyed the 14 existing SEO titles. Restored, then every mutation
passed `title` *and* `description`. Post-run check: 14 of 14 preserved.

### The copy

Descriptions were generated from each product's own body copy, which follows a
`<specs · line> <Name> — <selling sentence>` pattern, so the selling sentence was extracted and
composed as `<Product name> — <sentence>. Same-day London delivery.`

Three rounds of defect-hunting on the generated output, because meta descriptions are what
shoppers actually read in Google:

| Defect | Count | Action |
|---|---|---|
| Product name missing entirely | many | always lead with the name (Google bolds matched terms) |
| Spec-line fragment bleeding in (`James · First Served 1932 Very large…`) | 5 | hand-written |
| Clause trailing off mid-thought (`tastes, improbably, of pure.`) | ~10 | hand-written |
| Orphaned conjunction after the dash (`— and the single best thing`) | 10 | hand-written |
| Duplicate across two products | 1 | resolved by leading with the name |

A lowercasing heuristic was tried and **reverted** — it broke proper nouns (`suze is made from`,
`glera from the Veneto`, `italian heritage`). 27 of the 108 were ultimately hand-written from
source facts; the rest extracted cleanly.

Final: 108 descriptions, **84–158 characters** (median 139), zero duplicates, zero over 158,
every one naming the product.

### Verified live

Re-queried all 1,258 active products and re-ran the full Smart SEO resolution:
**0 render no meta description**, down from 108. Not inferred from `userErrors: []`.

Full manifest: `seo/aeo/bulk/product-meta-descriptions.csv`

---

## 2026-09-18 — Over-long product titles

### The brief was 303. The real number is 73, and the fix is not what it sounds like

Measured what actually renders in `<title>`, not the raw product title:

| | Count |
|---|---|
| Rendered `<title>` over 60 chars | **306** of 1,258 active |
| …of those, **product title is fine**; the ` \| Drinks House 247` suffix (19 chars) pushes it over | **233** |
| …of those, the **product title itself** is too long | **73** |

**The 233 were deliberately left alone.** Google cuts only the brand suffix on those — the
product name stays fully visible. "Fixing" them would mean deleting real search terms
(`70cl`, `Magnum`, vintages) to save characters that cost nothing:

> `Billecart-Salmon Elisabeth Salmon Rosé Champagne 2008 Magnum | Drinks House 247`
> → SERP shows `Billecart-Salmon Elisabeth Salmon Rosé Champagne 2008 Magnum…`

### Product titles were NOT changed

Product titles are customer-facing and informative on the page. Instead, a per-product
Smart SEO template (`product_seo/seo_tags`, timestamp above the bulk template) sets a short
**SEO title only**. 49 applied, all ≤60 chars, product titles untouched. The remaining 24
land at 61–68 chars, where compression would cost more identity than the extra characters
are worth, so they were left as-is.

The description slot of each template was populated with that product's **existing** meta
description, so the 108 descriptions fixed earlier today are preserved rather than blanked.

### Three iterations, because the first two produced bad copy

1. Hard word-boundary truncation: produced `…Dark, Milk and Pink Himalayan Salted` (loses
   "Caramel Truffles") and `…Chassagne-Montrachet 1er Cru Les` (ends on an article). Discarded —
   no better than letting Google truncate.
2. Token-priority compression, but the dash normaliser broke hyphenated names:
   `Chassagne-Montrachet` → `Chassagne - Montrachet`, `Billecart-Salmon` → `Billecart - Salmon`.
   Fixed by normalising only dashes that already carry whitespace.
3. Final pass caught two products compressing to the **same** title (the 15-piece and
   25-piece Les Cœurs boxes) — differentiated by piece count.

### The more valuable finding: hand-written SEO titles are being discarded

The bulk template's title slot is `${title}` — the **product title** — not
`${default-meta-title}`. So every `seo.title` written by hand in Shopify admin is ignored on
the 882 products the bulk template drives. Example: `moet-chandon-collection-imperiale`
already had a clean 50-character `seo.title`; the store was rendering the 62-character
product title instead.

Changing one field — the bulk template's title slot to `${default-meta-title}` — would make
every hand-written SEO title take effect store-wide, and turn "fix a title" into an ordinary
admin edit rather than a metafield operation.

**Not applied.** It rests on Shopify's `page_title` falling back to `product.title` when
`seo.title` is blank. That is documented behaviour and the variable is literally named
*default* meta title, but the blast radius is the `<title>` of every product page and the
egress proxy blocks this environment from loading a rendered page to confirm it. That check
takes about thirty seconds in a browser for someone who can open the site.

Manifest: `seo/aeo/bulk/product-seo-titles.csv` (49 applied, 24 left as-is).

---

## 2026-09-18 — Collection SEO metadata: complete

### Where the fix goes (different from products)

Read `snippets/smartseo.collection.metatags.liquid` rather than assuming the product
behaviour carried over. It doesn't. That file was corrected on 2026-08-06 and now ends:

```liquid
{%- assign meta_title = page_title | default: collection.title -%}
{%- assign meta_description = page_description | default: collection.description -%}
```

So collections render the **native Shopify SEO fields directly**, with the Smart SEO template
path computed and then discarded. Editing the native fields works — no metafield needed.
(The in-file comment records why: the 2022-era per-collection metafields were lower quality
than the SEO titles since written in admin, e.g. `/collections/champagne` metafield said
*"Buy Best Champagne Delivery in london."*)

### Applied — 62 collections, verified live

| | Before | After |
|---|---|---|
| SEO titles over 60 chars | 42 | **0** |
| Meta descriptions over 160 | 25 | **0** |
| No meta description at all | 3 | **0** |
| Duplicate titles / descriptions | — | **0 / 0** |

Every update passed **both** `title` and `description`, because `collectionUpdate` has the
same partial-input clobber behaviour proven on `productUpdate` earlier today — sending one
field nulls the other.

### Written by hand, not generated

Automated compression was tried and produced empty pipe segments
(`Laurent-Perrier Champagne Delivery London |  | Drinks House 247`) and left 10 still over
60, so all 42 titles were written by hand on a consistent pattern:
`<Category> Delivery London | Same Day 24/7 | Drinks House 247`. The boilerplate
`Same Day 30-45 Mins 24/7 | Drinks House 247` was eating 43 of the 60 characters; dropping
`30-45 Mins` recovered most of it without losing the speed promise.

Three further fixes caught in review before applying: two collections would have been given
an **empty** title (they had none, and "preserve current" resolved to `""`), and
`REPOSADO TEQUILA` was ALL CAPS.

Honest note on value: 13 of the 25 over-long descriptions were only 161–179 characters,
where Google truncates a couple of words at most. The real wins were the 210–326 character
ones (`italian-wine-gifts` at 326, `montrachet-wine-gifts` at 318), which lost whole
sentences.

Manifest: `seo/aeo/bulk/collection-seo-fixes.csv` — all 207 collections with current values.

---

## 2026-09-18 — Collection images: 186 → 2

Filled from product photography already in the store. **205 of 207** collections with
products now carry an image, up from 21.

### Selection was not "first product"

A naive first-product pick produced only **117 distinct images across 183 collections**
(the same bottle repeated wherever collections share a first product), and gave the
flagship `red-wine` collection a generic house product called *"Mixed Red"*.

Reworked to score candidates from each collection's first ten products, preferring a
product with a real brand (`vendor` not empty and not `Drinks House 247`) and penalising
generic titles, then assigning greedily so each collection takes an image nothing else has
used, largest collections choosing first. Result: **205 distinct images, zero reuse**, and
167 of the picks are branded bottles.

| Collection | Before | After |
|---|---|---|
| `red-wine` | *Mixed Red* (house generic) | Château les Eyquem Margaux 2021 |
| `cognac` | — | Hennessy |
| `gin` | — | Gordon's Dry Gin |
| `rye-whisky` | — | WhistlePig 10 Year Old |

Alt text is the collection title, not the product name — the image stands for the
collection.

### Two collections still have none, and the reason is a bigger problem

`lanson-champagne` and `wines-from-germany` each hold exactly one product, and **that
product has no photograph at all**:

- *Lanson Le Black Création 257 Brut NV Champagne 75cl*
- *J.J. Prüm Wehlener Sonnenuhr Riesling Kabinett 2023, 75cl*

A product with no image is a worse problem than a collection with no image: it will not
convert, and it cannot appear in Google Shopping or any agentic surface. Worth photographing.

### Operational note — `upstream_error` here does not mean failure

Setting `image.src` makes Shopify **fetch and re-host** the file server-side, so batches
time out at the response layer while the work completes. Four of the eight batches returned
`upstream_error`; verification showed every one had applied in full. Any retry would have
silently duplicated 20 image assets per batch.

**The rule: on `upstream_error` from an image-bearing mutation, re-query state before
retrying.** Batch 1 of 46 was the only genuine partial — 25 of 46 landed.

Manifest: `seo/aeo/bulk/collection-images.csv`.
