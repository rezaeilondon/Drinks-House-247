# "1.21K → 121 products synced" in the Agentic section — diagnosis

## The section is the Microsoft Copilot channel

| | |
|---|---|
| Channel | `gid://shopify/Channel/330936353143` |
| Name | Microsoft Copilot |
| Handle | `copilot` |
| App | `microsoft-1` |

**Correcting an earlier note in this repo:** a previous pass listed five sales channels and
said no agentic channel existed. That was wrong. It was drawn from `publications`, which
returns five. `channels` returns **six** — Copilot appears there and not in `publications`.
The earlier guess that the figure came from the Perplexity or Claude MCP app, or from
Marketplace Connect, was also wrong.

## Shopify's side is completely fine

```
published_status:330936353143-published  →  1,257
published_status:microsoft-1-published   →  1,257
```

**Every active product is published to the Copilot channel.** `productPublicationsV3`
shows them all `isPublished: true` with `publishDate` of **2026-08-07T23:56:31Z** onward,
timestamps one second apart — a single automated bulk publish when the channel connected.

Nothing has been unpublished, hidden, or removed since. The publication record is intact
and unchanged.

## Therefore the drop is on Microsoft's side, not yours

Shopify is offering 1,257 products. Microsoft is accepting 121. The ~1,136 difference is
**Microsoft rejecting products at ingestion**, which is not visible through the Shopify
Admin API — the rejection reasons live in Microsoft's own merchant systems.

## What is most likely driving it

Stated as likelihood, not fact. Only Microsoft's own rejection list can confirm.

1. **Alcohol is a restricted category for Microsoft.** This catalog is overwhelmingly
   alcohol — a 250-product sample returned champagne, whisky, vodka, gin, tequila, rum,
   cognac, wine, beer, liqueur, cider and aperitif. Microsoft Advertising restricts
   alcohol by market and generally excludes it from Shopping surfaces without specific
   approval. A policy tightening after launch would produce exactly this shape of drop.

2. **No product carries a GTIN.** 310 active published products sampled across two slices
   of the catalog: `barcode` is `null` on every one. Microsoft's feed spec expects a GTIN
   for branded manufactured goods, or an explicit declaration that none exists. Every
   bottle sold already has an EAN printed on it.

3. **The brand field is wrong on effectively the whole catalog.** `vendor` reads
   "Drinks House 247" on **1,253 of 1,257** active products. Shopify maps `vendor` to
   `brand`. Only four name a real producer: Rhum J.M, Clase Azul, Aberfeldy,
   R. López de Heredia Viña Tondonia.

Note what 121 is *not*: it is not the non-alcoholic subset. Mixers total 13, titles
containing "alcohol free"/"0.0" total 5, snacks 0. So this is not a clean
alcohol-rejected / everything-else-accepted split, and any explanation claiming so would
be wrong.

## What to do, in order

1. **Open the Copilot channel in Shopify admin and find its rejected or ineligible list.**
   Channels of this type report per-product reasons. That is the only authoritative answer
   and it beats anything inferable from outside.
2. **If the reason is alcohol policy**, this is not a data problem and no amount of feed
   work will fix it. The question becomes whether Microsoft will approve an alcohol
   retailer in the UK market at all.
3. **If the reason is feed quality**, fix GTIN and brand. Both are worth doing regardless,
   because they unlock matching on every agentic and shopping surface at once, not just
   this one. The vendor fix is largely mechanical: the producer is already the first words
   of most product titles.

## Unrelated findings worth knowing

- `autoPublish` is **false** on all six channels. Every new product must be published to
  each channel by hand or it reaches none of them.
- 26 products are published to no channel at all.
- 73 active, published products are out of stock, and most agentic surfaces drop those.

---

# Follow-up: hypotheses tested and ruled out (2026-09-17)

A set of plausible causes was proposed — a Liquid collection filter, a tag or metafield
condition, `published_scope`, or a hard-coded `first: 121` in a product query. All were
tested. **None holds**, and the first, second and fourth cannot hold in principle.

## Theme Liquid is not in the path at all

Microsoft Copilot is a **first-party Shopify sales channel**. It ingests product data
through Shopify's publication and channel APIs. It never renders the theme. Theme Liquid
drives the online storefront only.

So a collection filter in Liquid, a `collection.products` loop, or a hard-coded page size
in a template cannot affect what this channel receives. There is no template involved.
(The live theme was last updated 2026-09-15, after the channel's 2026-08-07 bulk publish,
which is why the idea was worth checking — but the mechanism does not exist.)

## "121 matches a collection size" — tested, false

All 214 collections were pulled and counted. **No collection contains 121 products.** The
nearest are 115 (`cabernet-sauvignon`), 114 (`wines-that-pair-with-lamb`),
112 (`chardonnay`) and 111 (`burgundy`). The sync is not scoped to a collection.

## `published_scope` — ruled out, and now properly validated

The earlier claim that all 1,257 active products are published to Copilot was previously
asserted from a single query. It has now been verified with a control:

| Channel | published | hidden | sum |
|---|---|---|---|
| Microsoft Copilot (330936353143) | **1,257** | 192 | 1,449 |
| Pinterest (118245163164) | 1,177 | 272 | 1,449 |
| Google & YouTube (58755481756) | 1,177 | 272 | 1,449 |
| Bogus channel ID (999999999999) | 0 | — | — |

Every real channel's published + hidden sums exactly to the 1,449 total, and an invented
channel ID returns zero. The filter is genuinely channel-aware, so the 1,257 is real.

**One red herring worth recording:** `resourcePublicationsV2` on individual products lists
only five publications and omits Copilot, which looks like a contradiction. It is not.
The session's access token cannot see Copilot's *publication* object — which is also why
`publications` returns five while `channels` returns six — but the channel-level data is
accessible and correct.

## Shopify holds no rejection feedback from this channel

Every per-product channel approval state returns zero:

```
294412484609-approved / rejected / needs_action / awaiting_review
              / published / demoted / provisionally_published   -> 0
error_feedback:*                                                -> 0
```

The Copilot channel does not write per-product status back to Shopify. **The reason for
the rejections exists only inside Microsoft's systems.** No amount of Admin API work will
surface it, which is why the channel's own admin page is the necessary next step rather
than a convenience.

(12 products sit in `intended` — added to the channel but not yet published. A rounding
detail, not the cause.)
