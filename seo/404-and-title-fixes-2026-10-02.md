# 404 links and doubled page titles — 2 October 2026

## 1. Broken internal links (404s)

Audit scope: every published page, published article, live product, collection
description and navigation menu (2,173 sources), checked against live pages,
Online Store products, collections, articles and URL redirects. `/ru/`, `/ar/`
and `/zh-cn/` prefixes were treated as valid (those languages are published).

**Before:** 34 links to 17 dead URLs, plus 3 redirects pointing at dead targets.
**After (re-audited from a fresh export):** 0 broken links, 0 bad redirects.

### Links fixed (23 items)

| Dead target | Why it 404'd | Replaced with | Where |
|---|---|---|---|
| Saint-Émilion Grand Cru Classé 2014 | draft | `/collections/red-wine` (image links) | online-wine-delivery-near-me…, red-wine-as-a-gift…, wine-delivered-in-london, wine-delivery-service-london, wine-gifts-delivered… |
| The Velvet Devil Merlot 2016 | draft | `/collections/merlot-wine-delivery`; Château Haut-Blanville Merlot | wine-delivery-24-hours; wine-delivery-near-me-now |
| Château Pontac-Lynch Margaux | draft | Château Labegorce Margaux 2022; `/collections/red-wine` (image) | alcohol-delivery-canary-wharf, instant-wine-delivery-near-me; indulge-with-wine-hampers… |
| Veuve Clicquot Rosé (old handle) | draft | `/products/veuve-clicquot-rose` (live listing of the same wine); `/collections/rose-champagne` for a generic anchor | same-day-champagne-delivery-london, anniversary-gifts collection; posts/how-to-choose-champagne |
| Freixenet Prosecco & Belgian Chocolate Handbag Gift | draft | Freixenet Prosecco D.O.C. & Scented Candle Gift Box (product + photo) for images/feature; `/collections/prosecco-gifts` for generic anchors | delivery-and-gift-services…, prosecco-as-a-gift…, wedding-anniversary-gifts-for-her…, wine-gift-box… |
| Madri Excepcional 24 × 440ml | ACTIVE but not published to Online Store | Heineken 440ml cans (text, FAQ, schema, image) | craft-beer-gift-sets-for-him… (my own earlier link) |
| Patrón XO Café | ACTIVE but not published to Online Store | Patrón Añejo card (live variant 42164751106204, £74.00) | tequila-delivery-london carousel — the old card's Add to Cart pointed at an unpublished variant |
| Havana Club Añejo Especial | draft | `/collections/rum` | posts/10-classic-cocktails-for-world-cocktail-day |
| Chablis Montée de Tonnerre 2023 | archived | `/collections/chablis` | posts/london-midnight-drinks-delivery |
| CoQ10 / shilajit / sea moss tablets | draft | links removed, words kept | mushrooms-supplements collection |
| Our COVID-19 Delivery Policy | page unpublished | new redirect → `/pages/alcohol-delivery` | html-sitemap |

Also removed from the mushrooms-supplements collection description: two pasted
copies of Twitter's site stylesheet (21 KB, including a global `body{margin:0}`).

### Redirects

| Path | Old target | New target |
|---|---|---|
| /products/prosecco-75cl-chocolate-handbag-gift-pallet-deal-147-units | /products/prosecco-75cl-chocolate-handbag-gift (draft) | /collections/prosecco-gifts |
| /products/rioja-denominacion-de-origen-calificada | /products/rioja-2013 (draft) | /collections/rioja |
| /pages/food-pairings-with-every-champagne | missing collection | /pages/champagne-pairing-guide-best-food-matches-uk-drinks-house-247 (page is live, so this redirect is dormant — fixed so it can't break later) |
| /pages/our-covid-19-delivery-policy | — (new) | /pages/alcohol-delivery |

The html-sitemap page still lists the COVID entry; it now resolves through the
redirect. Not rewritten because the page is 104 KB / 865 links.

## 2. "Drinks House 247" twice in page titles

**Cause:** the store name is saved as `"Drinks House 247 "` (trailing space).
The theme's SmartSEO page snippet appends ` – {{ shop.name }}` unless the page
title already contains the store name; because of the space, `…| Drinks House 247`
never matches, so 372 published pages render
`… | Drinks House 247 – Drinks House 247 `.

**Fix (owner action, cannot be done via API):** Settings → Store details → Store
name → delete the trailing space → Save. That fixes all 372 at once.

**Done via API:**
- 10 pages had stale SmartSEO overrides that hid their admin SEO titles. Both
  are now set to the same, corrected values (renders correctly with or
  without the store-name fix): alcohol-delivery-areas ("5 mile radius" removed),
  job and about-us ("DrinksHouse247" → "Drinks House 247"), challenge-25
  ("Challenge 21" → "Challenge 25" in title and description), contact-us,
  white-wine-delivery, 24-hour-alcohol-delivery-service, alcohol-delivery-bayswater
  ("Drink House" typo), food-pairing-veuve-clicquot, alcohol-gifts-the-perfect-gesture….
- Talisker 10 product SEO title: removed duplicated "| Drinks House 247".

Products, articles and collections: no doubled titles found.

## 3. Flagged, not changed

- **Challenge 21 vs 25:** the policy page (`/pages/challenge-25`) says Challenge 25,
  but 62 live pages/articles say Challenge 21 — including recent daily-blog posts,
  because `seo/daily-post-playbook.md` (lines 19 and 65) specifies Challenge 21.
  Needs the owner to confirm which policy applies; then fix site-wide and in the playbook.
- **Cash on delivery:** 25 pages (including about-us, contact-us and
  terms-and-conditions) mention paying cash, while structured data no longer lists Cash.
- **Product title tags ignore admin SEO titles:** the SmartSEO bulk template
  (`${title} | Drinks House 247`) and 493 per-product overrides take priority.
- **Mushrooms-supplements collection** makes health claims ("proven to strengthen
  immune systems", "reduce inflammation") that UK rules on supplement health claims
  do not allow, and still names CoQ10/shilajit/sea moss though those products are drafts.
- Some articles link to `/ru/` or `/ar/` versions of pages (work, but send English readers to translations).
