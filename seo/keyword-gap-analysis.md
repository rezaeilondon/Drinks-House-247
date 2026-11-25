# Drinks House 247 — Keyword Gap Analysis

**Date:** 2026-09-14
**Store:** drinkshouse247.co.uk (Shopify, GBP, London/BST)
**Catalogue:** 1,171 products — wine 434, champagne 262, tequila 123, whisky 88, gin 35,
vodka 32, cake 22, rum 20, spirits 16, soft drinks/mixers 30, chocolate 14, cognac 10, mezcal 7, flowers 4
**Existing content:** 418 pages, 263 blog articles (blog handle `posts`), ~500+ collections

---

## 1. What is already saturated — do NOT write more of this

The site has unusually deep commercial-intent coverage. These clusters are **done**; adding
more near-duplicates risks keyword cannibalisation rather than new traffic.

| Cluster | Evidence of saturation |
|---|---|
| Generic delivery intent | `alcohol-delivery`, `-service`, `-24-hours`, `-24-hours-1`, `instant-`, `late-night-`, `local-`, `same-day-`, `order-alcohol-online-near-me`, `booze-delivery-near-me` — 20+ near-duplicates |
| "Near me" pattern | Covered for alcohol, wine, beer, champagne, caviar, off-licence, shop |
| London areas | 24 borough pages: Mayfair, Chelsea, Kensington, Soho, Camden, Clapham, Battersea, Canary Wharf, Greenwich, Croydon, Ealing, Harrow, Richmond, Twickenham, Uxbridge, Paddington, Bayswater, Shepherds Bush, Peckham, Lewisham, Streatham, Kingston, Romford, Hammersmith |
| Occasions | Birthday, anniversary, wedding, engagement, housewarming, graduation, retirement, Valentine's, Father's Day, Mother's Day, Christmas, Easter, NYE, Dry January, hen party, office party |
| Gifting formats | Gift sets, hampers, baskets, personalised, corporate, bulk, last-minute, flute sets, chocolate pairings |
| Grape varieties | Pinot Noir, Cabernet Sauvignon, Merlot, Shiraz, Sauvignon Blanc, Pinot Grigio, Riesling, Malbec, Chardonnay, Chablis, Grenache, Rioja, Nebbiolo, Gewürztraminer, Tempranillo |
| Spirit categories | Whisky, vodka, gin, tequila, rum, cognac — each has a `-delivery-london` page |
| Caviar | Very deep: Beluga, Oscietra, Kaluga, Baeri, Almas, Prunier + 4 area pages |
| International send-to-UK | USA, Canada, Australia, Europe, China/HK, Singapore, Saudi Arabia, UAE |
| Champagne houses | Veuve Clicquot (7 pages), Dom Pérignon, Moët, Bollinger, Ruinart, Laurent-Perrier, Pol Roger, Cristal, Piper-Heidsieck, Armand de Brignac, Charles Heidsieck |
| Tequila gifting | 10+ pages (`send-tequila-gift-uk`, `tequila-gifts-for-him/her`, Cazcanes, etc.) |

## 2. The real gaps

### GAP A — Answer-engine (AEO/GEO) content — **primary focus**

This is the largest and most valuable gap. The existing 418 pages are written as
*commercial* pages: keyword-led headings, promotional prose, no direct answers.
Large language models (ChatGPT, Perplexity, Google AI Overviews, Copilot) cite pages that:

- answer a question **in the first 40–60 words**, before any selling;
- state **checkable specifics** (times, prices, units, distances, legal rules);
- carry **structured data** (`FAQPage`, `Article`, `LocalBusiness`) so the answer is machine-extractable;
- use **comparison tables**, which models lift almost verbatim;
- name the **entity** consistently ("Drinks House 247, a 24-hour alcohol delivery service in London").

Almost none of the current content does this. Fixing it is the cheapest route to
appearing in AI answers, because the commercial authority already exists.

### GAP B — Service-logistics questions (zero coverage)

Real London questions nobody on the site answers, all with commercial intent behind them:
3am ordering, hotel/Airbnb delivery, office delivery, ID at the door, nobody-home policy,
Christmas Day, minimum order, licensing hours. These are exactly the questions
people ask assistants rather than search engines.

### GAP C — Premium brand entities (deep stock, no pages)

Stocked in depth but with **no dedicated page or article**:
Macallan (19 products — the single largest branded line), Clase Azul (12), Belvedere (10),
Krug (8), Casa Dragones (6), Komos (5), Volcán (5), G4 (5), Cazcanes (5), Salon (4),
ArteNOM (4), Herradura (4), Don Julio (4), 818 (4), Louis Roederer (3), Mijenta (3).
Brand + comparison queries ("Macallan 12 vs 18", "Clase Azul vs Don Julio 1942")
are high-intent and heavily asked of LLMs.

### GAP D — Quantity & planning maths

"How many glasses in a bottle", "how much champagne for 50 guests", "how many bottles
per person at a wedding". High-volume, evergreen, endlessly cited by AI answers, and they
lead naturally to bulk/case products. Only one adjacent article exists (ice for a party).

### GAP E — Cake, flowers & pairing bundles

22 cakes, 14 chocolate lines, 4 flower lines in stock. Only `engagement-flowers` and
`flowers-and-wine-delivery` exist. "Birthday cake and champagne delivery London" is uncontested.

### GAP F — Mezcal & lesser spirits

7 mezcal products, zero content. Cognac has a delivery page but no brand or comparison content.

## 3. Strategy

1. **Daily article** on the `posts` blog, drawn from `seo/backlog.json`, written to the
   AEO template in `seo/daily-post-playbook.md` (direct answer first, table, FAQ, JSON-LD).
2. **Answer hub landing page** interlinking the answers so crawlers and models find a
   single authoritative entity page — and so each daily post has a parent to link to.
3. Every post links to real collections/pages, building internal PageRank toward
   commercial pages that already rank.

## 4. Measurement

Watch in Google Search Console: impressions for question-shaped queries, and pages
gaining impressions without clicks (a signature of AI-answer surfacing). Re-run this
gap analysis quarterly as the backlog drains.
