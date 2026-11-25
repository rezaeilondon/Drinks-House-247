# Audit of all 421 pages — 2026-09-18

Every page body was extracted, de-HTML'd and compared against every other
(87,990 pairwise comparisons on 6-word shingles), plus intent clustering on
title keyword signatures and an inbound-internal-link count across 2,164 source
documents (pages, collections, articles, product descriptions).

## The hypothesis I raised was wrong

I flagged a likely **doorway-page cluster** on the grounds that the redirect table is
full of already-consolidated near-duplicates (`champagne-gift-delivered`,
`champagne-sent-as-a-gift`, `champagne-delivered-as-a-gift`, `deliver-champagne-gift`…).
Measured, that is not what is on the site now:

| Body overlap (Jaccard) | Pairs |
|---|---|
| ≥ 0.50 | **1** |
| 0.35 – 0.50 | 40 |
| 0.25 – 0.35 | 61 |
| 0.15 – 0.25 | 340 |

One pair out of 87,990 crosses 0.50. The 22 `alcohol-delivery-<borough>` pages — the
obvious doorway candidate — have a **median pairwise overlap of 0.00** and a max of 0.47,
with only 12 of 378 pairs above 0.40. They are genuinely distinct local pages, not
spun templates. Content depth is also sound: median **479 words**, p25 387.

**Conclusion: there is no doorway problem.** The consolidation visible in the redirect
table appears to be work someone already did correctly.

## Real finding — keyword cannibalisation (26 pages, 8 clusters)

Distinct *content*, identical *intent*. These pages compete with each other for the same
query, splitting link equity and leaving Google to pick.

| Cluster | Pages | Strongest (by inbound links) |
|---|---|---|
| wine next-day / same-day delivery | **6** | `next-day-wine-delivery` (17 inbound) |
| same-day champagne delivery | 5 | `champagne-shop-near-me` (3) |
| send tequila as a gift | 4 | `tequila-birthday-gift-uk-luxury-tequila-gifts` (3) |
| send a champagne gift | 3 | `send-a-gift-of-champagne` (19) |
| beer delivery near me | 2 | `online-beer-delivery-near-me` (3) |
| 24-hour alcohol near me | 2 | `alcohol-24-hour-near-me` (3) |
| alcohol as a gift | 2 | `alcohol-delivery-as-a-gift` (2) |
| champagne gift next-day | 2 | `champagne-gift-delivery-same-day-…` (1) |

Full table with word counts and link counts: `seo/aeo/bulk/page-cannibalisation.csv`.

**Important nuance for whoever consolidates:** strongest-by-links is not
strongest-by-content. In the wine cluster `next-day-wine-delivery` holds 17 inbound links
on 364 words, while `london-wine-delivery-same-day` has 1,000 words and 1 inbound link.
The right move is to keep the URL that holds the equity and merge the better body into it —
not to keep whichever page reads best.

Not actioned here: consolidation means redirecting live URLs and merging copy, which is a
commercial judgement about which pages matter, not a mechanical fix.

## Real finding — 39 pages under 300 words

Several are legitimately short (policy pages, `job`). But roughly 15 are **commercial
landing pages** too thin to rank:

| Words | Page |
|---|---|
| 179 | `alcohol-gift-hampers-uk-luxury-bundles-hampers-delivery…` |
| 201 | `graduation-celebration-drinks-delivery` |
| 203 | `fine-wine-gift-delivery-uk-premium-red-white-wine-gifts…` |
| 205 | `caviar-delivery-knightsbridge` |
| 207 | `whisky-gift-sets-uk-premium-scotch-blends-delivery…` |
| 237 | `caviar-delivery-chelsea` |
| 249 | `wedding-anniversary-wine-and-champagne-delivery` |
| 259 | `shiraz-wine-delivery` |
| 261 | `rum-delivery-london` |

## Housekeeping

**3 genuinely unpublished pages** (verified live, not from cache):
`our-covid-19-delivery-policy` (240w), `sca-affiliate-empty-page` (**0 words**),
`sending-champagne-as-gift` (465w, correctly superseded by a redirect).
The empty affiliate page and the COVID policy are candidates for deletion.

A fourth page my cached snapshot listed as hidden —
`fine-wine-vintage-spirits-the-complete-investment-gifting-guide-for-uk-collectors` —
is **published** on the live store (since 2026-06-26). The cache was stale; re-checked
before reporting, because a redirect does point at it.

**Orphans: effectively none.** Exactly 1 of 417 published pages has zero inbound links
from site content — `html-sitemap`. Caveat: this scan covered content bodies only, not
theme templates, so it may well be linked from the footer in Liquid.
