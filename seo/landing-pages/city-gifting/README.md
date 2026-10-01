# International gifting landing pages

"Send a gift to London from <city>" pages for overseas senders, the eight country pages they hang off, and one hub
that links them all. All are live. `pages.json` holds the Shopify page IDs, handles and SEO title/description for the
city pages and the hub; `country-pages.json` does the same for the country pages. Each `<handle>.html` is the live body.

## Hub
`/pages/send-gifts-to-london-from-abroad` (published 2026-10-01) lists every country and city guide. Every city and
country page links back to it.

## City pages (23)
| Region | Cities | Added |
|---|---|---|
| USA | New York, Beverly Hills & LA, Miami & Palm Beach, San Francisco | batch 1 |
| USA | The Hamptons, Greenwich (CT), Chicago, Dallas & Houston | batch 2 |
| Canada | Toronto | batch 1 |
| Europe | Paris, Monaco | batch 1 |
| Europe | Geneva & Zurich, Milan | batch 2 |
| Gulf | Abu Dhabi, Doha | batch 1 |
| Gulf | Riyadh, Kuwait City | batch 2 |
| Asia | Hong Kong, Tokyo | batch 1 |
| Asia | Shanghai, Mumbai | batch 2 |
| Australia | Sydney | batch 1 |
| Australia | Melbourne | batch 2 |

Batch 1 published 2026-10-01 (early hours); batch 2 and the hub published 2026-10-01 (evening).
Singapore and Dubai have no separate city page: their country pages are already city-specific, so a second page
would compete with them. Those two country pages were rewritten around the city instead.

## Country pages (8, rewritten 2026-10-01)
USA, Canada, Australia, Europe, China & Hong Kong, Singapore, Saudi Arabia, UAE & Dubai. Handles unchanged.
The previous copy was thin and repetitive and promised "next-day UK-wide" and "free delivery on qualifying orders";
both are gone. Each page now has a time-zone table, what senders there choose, how to order, an FAQ and its city
guides. Saudi Arabia and UAE pages are retitled "Send Gifts to the UK from …" and lead with alcohol-free gifts.
Pre-rewrite bodies are in the session scratchpad only (`country/expected.json`, `new` field).

## Facts used on every page
Licensed dispatch unit in Battersea (not a shop); London delivery 24/7, typically 30–45 minutes; mainland UK express
1–2 / standard 3–5 business days; checkout in GBP; stock from HMRC AWRS-approved UK wholesalers with UK duty paid;
Challenge 25. Riyadh and Kuwait City lead with alcohol-free gifts (alcohol is prohibited in both countries); champagne
is offered only "for recipients in London who drink".

## Checks done
- All 95 link targets in batch 2, the hub and the country rewrites were checked live: 18 products ACTIVE and
  published to the Online Store, 42 collections non-empty, 35 pages published.
- Every live body was read back and compared with what was sent: 31 of 32 match exactly. The USA country page
  differs only by a newline Shopify inserts inside `<li><strong>`.
- Time tables checked per city, including the US/UK and Australia/UK daylight-saving offsets.

## Link from older batch-1 pages
The 12 batch-1 city pages each gained one closing line linking to the hub (no other change).

## Watch
- Kweichow Moutai (linked from Shanghai and China/HK) had 1 bottle in stock on 2026-10-01.
