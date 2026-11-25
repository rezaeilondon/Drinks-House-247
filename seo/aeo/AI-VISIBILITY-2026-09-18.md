# What AI crawlers and LLMs actually see — audit, 2026-09-18

Follows `ai-crawler-audit-2026-09-17.md`. Same hard limitation: **the live site cannot be
fetched from this session.** The egress gateway returns 403 to CONNECT for both
`drinkshouse247.co.uk` and `cdn.shopify.com`, and a blocked host is reported rather than
routed around. Everything below is from the Shopify Admin API — theme source, shop
metafields, app config, and the `descriptionHtml` of all 1,258 active products.

Two things that were blocked and are therefore *not* done, rather than done badly:

- `bulkOperationRunMutation` is refused by the MCP safety policy, so a 1,247-product
  update cannot be shipped as one bulk job.
- Theme writes to the live theme are blocked, so `templates/robots.txt.liquid` still
  cannot be added.

---

## 1. Every product reads as a blob of CSS — the headline finding

`templates/llms.txt.liquid` (158,917 bytes) is the file LLM crawlers are pointed at. Its
product section renders like this, for **213 of the 213 products that carry a description**:

```
### [Grey Goose Vodka 70cl](https://drinkshouse247.co.uk/products/grey-goose)
- Type: vodka
- Vendor: Drinks House 247
- Description: @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond…
  #dh247-pd{--ink:#1a1a1a;--ivory:#faf7f0;--line:#e4ded0;--accent:#8b6f3e;font-family:…
```

The generator strips HTML tags but keeps the *text content* of `<style>`, then truncates
at roughly 300 characters. Because the `<style>` block sits at the very start of
`descriptionHtml`, the truncation window is consumed entirely by CSS. Not one product
communicates a single fact about what it is.

Measured across all 1,258 active products:

| | count | share |
|---|---|---|
| carry a `<style>` block in `descriptionHtml` | 1,248 | 99.2% |
| …with the style block *leading*, before any prose | 1,232 | 97.9% |
| genuinely clean | 9 | 0.7% |
| empty description | 1 | — |

The copy underneath is good and is being wasted: after stripping tags and CSS, the
remaining prose runs **826 characters at the shortest, 1,836 median, 7,810 longest**.
Nothing is under 200 characters. This is a delivery defect, not a content problem.

The same `descriptionHtml` is what `/products/{handle}.json`, the UCP `search_catalog`
tool, and the Google Merchant feed all read.

### The fix, and why it is not applied yet

Verified transformation, byte-checked against all 1,248: remove the embedded JSON-LD
(see §2), lift the `<style>` block out and re-append it at the end of the field. Prose is
byte-identical before and after; every one of the 49 distinct CSS blocks survives verbatim;
0 safety failures. CSS applies identically wherever it sits in the body, so rendering does
not change.

The 49 CSS variants share the same `#dh247-lux` / `#dh247-pd` selectors but are genuinely
different (similarity to the most common block is 0.25 or lower for most). They therefore
**cannot** be merged into one stylesheet without changing how products look.

A canary was applied and verified — `water-1-5l`, SEO title, SEO description, tags, vendor,
product type and status all intact, confirming `descriptionHtml` alone does not clobber
neighbouring fields the way `seo:{description}` alone clobbers `seo.title`.

The remaining 1,247 are prepared and validated in the session scratchpad (`plan.json`,
`desc.jsonl`, 10.5 MB) with originals backed up (`originals.json.gz`). Delivery is the
blocker, not correctness: the bulk mutation endpoint is refused by policy, so this has to
go through per-product mutations.

## 2. 1,245 products still carry a frozen, hand-written Product schema

`snippets/dh247-clean-description.liquid` strips these at render, so browsers and Google's
page crawl are clean. **The blocks are still in the product records**, so every feed and
data consumer still reads them. Checked against live prices:

- **15 products state a price that contradicts the live price.**
  Worst: Don Julio 1942 Tequila 70cl says `225.00`, live is `165.00`. Dom Pérignon Vintage
  2008 says `366.00`, live is `395.00`. Kweichow Moutai Flying Fairy says `525.00`, live
  is `499.00`. Full list in `schema-price-mismatch.csv`.
- **2 products declare `InStock` for something unpurchasable** —
  `rhum-j-m-vsop-rhum-agricole-vieux-70cl` and
  `indri-diwali-collectors-edition-indian-single-malt-whisky-70cl`.

These do not reach llms.txt, because the 300-character truncation cuts off long before the
schema block at the end of the field. The exposure is raw product JSON and anything reading
the API directly.

## 3. /llms.txt serves a two-month-old snapshot

```
{"path":"/llms.txt","target":"https://cdn.shopify.com/s/files/1/1624/5203/files/llms.txt.txt?v=1784248418"}
```

`v=1784248418` is **2026-07-17**. The template it bypasses regenerated on **2026-09-15**
(`> Last updated: 2026-09-15` on line 4). So the redirect serves a frozen July file while a
fresher one sits unused.

**Not deleted, deliberately.** Shopify does not route arbitrary template filenames, so the
redirect may be the only thing making `/llms.txt` resolve at all — removing it could turn a
stale file into a 404, which is worse. This needs one browser check to resolve, see §7.

`templates/llms-full.txt.liquid` (158,927 bytes) has **no redirect at all** and is byte-identical
to `llms.txt.liquid` apart from the marker comment, so it is both unreachable and redundant.

## 4. llms.txt covers 214 of 1,258 products

The file's own header: `Products: 214 | Collections: 42 | Articles: 27 | Blogs: 2 | Pages: 15`.
That is **17% of the active catalogue**. Collections, articles, blogs and pages are complete;
products are not. No shop metafield controls this — the cap is internal to the Smart SEO app,
so it is a dashboard setting or a plan limit. Worth checking in the app, because it is the
single cheapest large win available: the other 1,044 products are simply absent from the
feed LLMs are pointed at.

## 5. A second SEO app was contradicting the identity fix — corrected

A `store_seo` namespace holds nine schema configs, all `status: true`, publishing alongside
Smart SEO. Its organisation schema carried a **different set of social accounts** from the
ones the owner confirmed on 2026-09-17, so every page asserted both:

| | was (store_seo) | now |
|---|---|---|
| instagram | `instagram.com/drinkshouse247.co.uk/` | `instagram.com/drinks.house.247/` |
| twitter/x | `x.com/DrinksHouse247` | `x.com/drinks_house247` |

`sameAs` is among the strongest identity signals available, and it was self-contradicting
on every page — which undid the 17 September correction. **Fixed.**

Also fixed in the same app: `"shippingCurrency":"GPB"` → `"GBP"`. `GPB` is not a currency
code, so the shipping details in merchant schema were invalid.

Left alone deliberately: the Facebook, Pinterest and LinkedIn URLs. The two apps disagree on
Facebook and I have no confirmed answer, so guessing would just move the contradiction.

## 6. Still open, unchanged from 17 September

- **`shop.name` is `"Drinks House 247 "`** — trailing space, admin-only. It is written into
  the `name` of the Organization on every page, and it also appears in the generated
  `agents.md`: *"Agent Instructions — Drinks House 247 "*.
- **`EnableStoreAddress` / `EnableStructuredDataForRealStore` are both `false`** in Smart SEO,
  because the billing address is malformed for schema use (`city` = `"Battersea, london"`).
  Note that LocalBusiness markup **is** being published by `store_seo`, with a better-formed
  address, so this is less urgent than it looked.
- **No `templates/robots.txt.liquid`.** The store serves Shopify's stock robots.txt, which
  does not name AI crawlers. Theme writes to the live theme are blocked here.
- **`agents.md` is healthy.** Shopify-generated, 8,931 bytes, covering UCP discovery, the MCP
  endpoint, the Shop skill and read-only browsing. Nothing to do.

## 7. The one thing worth thirty seconds in a browser

Open **`drinkshouse247.co.uk/llms-full.txt`**.

- **It loads** → Shopify routes these templates natively, the `/llms.txt` redirect is pure
  harm, and deleting it makes `/llms.txt` serve the fresh file immediately.
- **It 404s** → the redirect is the only delivery mechanism, and the fix is to get Smart SEO
  to re-upload a current snapshot instead.

Same visit, check `drinkshouse247.co.uk/robots.txt` for `GPTBot`, `ClaudeBot`,
`PerplexityBot`, `CCBot` or `Google-Extended` under a `Disallow: /`.
