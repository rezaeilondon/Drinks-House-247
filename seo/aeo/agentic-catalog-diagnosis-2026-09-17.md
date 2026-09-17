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
