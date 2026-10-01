# Internal-linking quick wins — 2026-10-01

Scope: 1,241 live product descriptions, 270 published articles, 417 published pages, 214 collection
descriptions, the main/footer menus and 775 URL redirects. Full per-link list:
`link-issues-2026-10-01.csv`.

## Priority 1 — sitewide menus (every page, ~10 edits)
- Main menu "Rosé Champagne" uses an absolute https URL, so localised visitors (/ar/ /ru/ /zh/, 48% of sessions) drop back to English.
- Footer "Challenge 21" links to /pages/challenge-25.
- Gift menu labels point at generic categories: "Wine Gifts" → /collections/wines, "Spirits Gifts" → /collections/liquor, "Gin Gifts" → /collections/gin, "50th Birthday Champagne" → champagne-gifts.
- Footer-3/footer-4: eight different area anchors ("Beer Delivery SW1", "Drinks Delivery Camden", ...) all point to /pages/alcohol-delivery-areas.
- "Alcohol Delivery Near Me" → /collections/all-products.
- Beer has no submenu; Mixers is not in the main menu.

## Priority 2 — links to hidden products (119 links on 98 pages)
- 70 product pages carry a cross-sell card for `exotic-fruits-delight-basket-premium-assortment`, which is DRAFT (12 in stock), so the card 404s. All 70 are in the 182 not-yet-rewritten descriptions.
- 49 more links go to draft or archived products (Veuve Clicquot 2008, Veuve Clicquot Rosé, Freixenet handbag gift, Saint-Émilion 2014 and others). Patrón XO Café is ACTIVE with 12 in stock but is not published to the Online Store.

## Priority 3 — redirect hops (517 links on 267 pages, 71 targets)
Each link passes through a 301. Rewriting it to the final URL is mechanical and safe. Top targets:
- 86 links → /products/untitled-jun7_02-52-44 (→ the-celebration-hamper)
- 62 links → /collections/champagne/products/dom-perignon-champagne (→ dom-perignon-champagne-2013)
- 74 links → /products/untitled-jun13_* (→ Seventy One gift sets)
- 32 links → /pages/delivery-info (→ /policies/shipping-policy)
- 30 links → the old Charbonnel Union Jack handle

By source: 262 links in pages, 188 in products, 48 in articles and 19 in collections.

## Priority 4 — true 404s and tag URLs
- Four links have no page and no redirect:
  - /blogs/posts/hennessy-history-what-it-is-made-from-prices-in-london (in hennessy-vs-vsop-xo-difference)
  - /blogs/posts/beautiful-wine-rack-ideas-for-your-home (in html-sitemap)
  - /collections/champagne/products/Bollinger (in champagne-delivery)
  - /collections/Champagne (in gift-congratulations-...)
- About 25 tag-filter URLs such as /collections/blanco-tequila/Blanco-Tequila and /collections/champagne/veuve-clicquot should become their real collection URLs.

## Priority 5 — product pages link nowhere
1,081 of 1,241 live product descriptions have no internal link. Proposed fix: add one closing line linking the brand collection and the category collection, chosen from each product's existing collection membership.

## Priority 6 — collection hubs
- 61 collection descriptions link nowhere. Examples: vintage-wine (507 products), champagne-standard-bottle-75cl (255), single-malt-whisky (94), champagne-flute-gift-sets (91) and gifts-hampers (37). Adding 2–3 sibling and guide links per hub would help.
- Seven collections are empty: doux-champagne, practicing-biodynamic-wines, carbon-neutral-wines, sparkling-red-wine, viognier, torrontes and sardinia. They are thin pages: either fill them or unpublish them.
- Two one-product collections (lanson-champagne, wines-from-hungary) have no inbound links.

## Priority 7 — absolute internal links (locale leak)
- 8,241 internal links are absolute (`https://www.drinkshouse247.co.uk/...`): 5,409 in pages, 1,654 in products, 871 in articles and 307 in collections.
- Each one sends a /ar/, /ru/ or /zh/ visitor back to English.
- The three top-traffic articles already use relative links.

## Priority 8 — inert redirects (153 links to 21 live pages)
These pages are live, so their redirects never fire. Examples: /pages/alcohol-delivery-areas (55 links), next-day-wine-delivery, wine-delivery-london, wine-delivery-london-same-day and champagne-delivery.

For each page, decide: keep it and delete the redirect, or unpublish it so the redirect consolidates its signals into the collection.

## Checked and fine
- Every live product is in at least one real collection.
- Every collection has a meta description.
- Every published article has internal links.
- The top-traffic articles (least-calories, flowers-and-champagne, drinking-games) have 8–23 relative links each.

## Applied 2026-10-01 — menus (Priority 1)
- Main menu: "Rosé Champagne" now links to the collection (works in every language); "Gin Gifts" → /collections/gin-gifts; "Wine Gifts" → /pages/wine-gifts; "50th Birthday Champagne" (it pointed to generic champagne gifts) replaced with "Thank You Gifts" → /collections/thank-you-gifts; Beer now has a dropdown: All Beer, Soft Drinks & Mixers, Beer Delivery London.
- Footer + Quick Links: "Challenge 21" renamed "Challenge 25".
- Footer-2: "50th Birthday Champagne" renamed "Champagne Gifts London" (same target).
- Footer-3: "Beer Delivery SW1" → "Beer Delivery London" (/collections/beers); "Drinks Delivery SW11" → "Drinks Delivery Chelsea" (/pages/alcohol-delivery-chelsea); "Drinks Delivery Service" → /pages/alcohol-delivery-service; "Late Night Booze Delivery" → /pages/late-night-alcohol-delivery.
- Footer-4: Camden, Kensington, Clapham, Battersea now go to their own area pages; added Alcohol Delivery Mayfair and Alcohol Delivery Soho.
- Delivery menu: "Alcohol Delivery Near Me" → /pages/alcohol-delivery.
- Not changed: "Spirits Gifts" and "Tequila Gifts" (no dedicated gift collection exists).

## Prepared, not yet applied — content link fixes (Priorities 2–4)
`link-rewrite-map-2026-10-01.csv` lists every href change (446 distinct pairs). Scope: 82 products (188 links, plus removing 70 Exotic Fruits basket cards), 136 pages (317 links), 50 articles (64 links), 14 collections (19 links).

## Applied 2026-10-01 — collections
All 14 collection descriptions updated (19 links) and verified against live: links match exactly; three non-breaking spaces in brut-champagne and blanc-de-blancs-champagne became plain spaces (no visible change).

## Blocked — bulk updates
The Shopify connector refuses `bulkOperationRunMutation` ("Bulk mutation operations are blocked"). Products (82), pages (136) and articles (50) remain to apply one by one.

## Folded into the rewrite plan
`plan.json.gz` `new` descriptions for the 79 not-yet-rewritten affected products now carry the same link fixes and have the 70 Exotic Fruits basket cards removed (they previously would have re-published them).

## Applied 2026-10-01 — Exotic basket redirect
Added redirect `/products/exotic-fruits-delight-basket-premium-assortment` → `/collections/gifts-hampers` (UrlRedirect 1735387218295). The product is DRAFT, so the 70 cross-sell cards now land on Gifts & Hampers instead of a 404 until the rewrite removes them.
