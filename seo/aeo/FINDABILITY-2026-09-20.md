# Can humans and AI bots find the store? — audit, 2026-09-20

## Verdict

Yes for the storefront and, as of today, for the catalog. Two real gaps were
found; one is fixed, one is a merchandising decision and is listed below.

## What is working

| Check | Status |
|---|---|
| `/llms.txt` | **Fixed today** — 739,775 bytes, 1,242 products (was a 1,439-byte stub) |
| `/llms-full.txt` | **Added today** — resolves to the same catalog |
| robots.txt blocking AI crawlers | No. `templates/robots.txt.liquid` does not exist, so the store serves Shopify's stock robots.txt, which does not disallow `GPTBot`, `ClaudeBot`, `PerplexityBot`, `CCBot` or `Google-Extended` |
| `noindex` on products | None. `smartseo.no.index` only fires for search templates and tag-filtered URLs |
| `noindex` on collections | None. The snippet is *included* on collection templates but its conditions are `NoIndexSearchPage` (false) and `NoIndexTagPages` (false) |
| Products on the Online Store | 1,243 of 1,258 active |
| Products on Google & YouTube | **1,250 of 1,258** (was 1,178 before today) |
| Structured data | `EnableStructuredData: true` — Product, Collection, Breadcrumb and Organization JSON-LD all emitting |
| Social profile links in schema | Correct (`drinks.house.247`, `drinks_house247`) |

## Fixed today: 78 products were invisible to Google

80 active products had never been published to the Google & YouTube channel —
so they were absent from Google Shopping and Google free listings entirely.
They were not obscure lines; they included:

- Dom Pérignon Vintage 2017 Gift Box (264 in stock)
- The Murakami Prestige Hamper, The Malt Collector's Hamper, The Cristal
  Prestige Hamper, The Great British Hamper
- The whole Kosher range (Herzog, Carmel, Yatir)
- López de Heredia Viña Cubillo 2014 and 2017
- Redbreast 12, Green Chartreuse, Bowmore 21, WhistlePig 10, Grey Goose Altius

78 of the 80 were published to Google (all returned empty `userErrors`). The
remaining 2 were deliberately skipped — see below.

## Open: 15 active products are not published to the Online Store

These are invisible to everyone — not on the site, not in search, not in
`llms.txt`. Several carry real stock, so this looks unintended rather than a
deliberate delisting. This is a merchandising call, so nothing was changed.

| Product | Stock | Added |
|---|---|---|
| Champagne Pierre Péters `Les Montjolys` Blanc de Blancs 75cl | 18,000 | 2023-08-24 |
| Thorne & Daughters `Snakes & Ladders` Sauvignon Blanc 2021 | 13,000 | 2023-09-15 |
| Macon Lugny 2022 | 4,000 | 2023-12-29 |
| Maison Caroline Lestimé Bourgogne Hautes Côtes de Beaune Rouge 2020 | 4,000 | 2024-03-13 |
| Madri Excepcional Lager 24x 440ml Cans | 100 | 2022-11-11 |
| Patron XO Cafe Tequila | 12 | 2018-12-23 |
| Journeyman Russian River Chardonnay 2020 | 10 | 2023-09-12 |
| Dom Ruinart 2010 | 6 | 2024-04-07 |
| Clos De Tart Grand Cru Monopole 2012 | 6 | 2024-07-20 |
| Macallan 18 Year Old Double Cask 70cl | 4 | 2025-05-21 |
| Moët & Chandon Grand Vintage Collection 1978 Magnum | 1 | 2024-07-20 |
| Maison Caroline Lestimé Chassagne-Montrachet 2018 | 0 | 2024-03-13 |
| Saint Georges Cote Pavie 2012 | 0 | 2024-04-13 |
| Charles Heidsieck Brut Millésime 1981 (1.5L) | 0 | 2024-07-20 |
| Luce 2019 | 0 | 2024-08-06 |

11 of these are also off the Google channel. They were **not** published to
Google: a product with no storefront page gives Google a destination URL that
does not resolve, which risks a Merchant Center disapproval rather than a
listing. Publish them to the Online Store first, then to Google.

## Worth considering

- **Tag pages are indexable.** `NoIndexTagPages` is `false`, so every
  `/collections/x/tag-y` URL is crawlable. That multiplies near-duplicate pages
  and is a plausible contributor to the 26 cannibalising pages already logged.
  Turning it on is a Smart SEO setting.
- **`shop.name` is `"Drinks House 247 "`** with a trailing space. It feeds
  `${shop-name}` in every SEO title template. Admin-only fix.

## Not verifiable from here

Outbound HTTPS to `drinkshouse247.co.uk` and `cdn.shopify.com` is refused by
this environment's egress proxy (403 on CONNECT). So every statement above is
from the Shopify Admin API and theme source, not from fetching live URLs.
Specifically unconfirmed: that `/llms.txt` renders correctly in a browser, and
that `/agents.md` resolves at all — `templates/agents.md.liquid` exists but has
no redirect, which is the same shape as the llms.txt defect.
