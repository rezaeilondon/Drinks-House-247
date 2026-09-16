# Redirect audit — 2026-09-16

Checked after the owner reported "fixed all redirections on all pages".
**749 URL redirects** now exist on the store. Sampled the first 50 matching `pages`.

## 1. The newest redirects are inert

Shopify fires a URL redirect **only when the requested path 404s**. A published page
always wins. Every redirect below points away from a page that is still live and
published, so none of them fire and both pages keep competing:

| Redirect | Source page status |
|---|---|
| `/pages/champagne-same-day` → `/pages/champagne-delivery` | live, published |
| `/pages/champagne-delivery-to-me-same-day` → `/pages/champagne-delivery` | live, published |
| `/pages/next-day-wine-delivery` → `/pages/wine-delivery-london` | live, published |
| `/pages/buy-wine-next-day-delivery` → `/pages/wine-delivery-london` | live, published |
| `/pages/next-day-wine` → `/pages/wine-delivery-london` | live, published |
| `/pages/wine-near-me` → `/pages/wine-delivery-london` | live, published |
| `/pages/alcohol-delivery-areas` → `/pages/alcohol-delivery` | live, published |
| `/pages/food-pairings-with-every-champagne` → a collection | live, published |

Fix: unpublish or delete the source page. The redirect activates the moment the page
stops resolving.

## 2. One redirect points at a target that does not exist

`/pages/food-pairings-with-every-champagne` → `/collections/champagne-gifts-luxury-champagne-gift-delivery-in-london-uk`

That collection handle returns nothing. Harmless today only because the redirect is
inert. Unpublish the page and every visitor lands on a 404 — and this is the Chinese
page carrying 40 sessions a quarter, whose internal links were repaired on 14 September.

## 3. Two live redirect chains

- `/pages/unique-alcohol-gift-sets-for-any-occasion` → `/pages/alcohol-gift-for-any-occasion` → `/pages/alcohol-gift-any-occasion`
- `/pages/champagne-gifts-for-birthday-celebrating-with-bubbles` → `/pages/champagne-gifts` → `/pages/champagne-gifts-birthday`

In both cases the middle page has been deleted, so the first hop fires and lands on a
second redirect. Point the first hop straight at the final destination.

## 4. Direction disagrees with the consolidation plan

`/pages/alcohol-delivery-areas` → `/pages/alcohol-delivery` runs opposite to
`delivery-consolidation-plan.json`, which folds the 16 borough pages *into*
`alcohol-delivery-areas` as the hub. Whichever direction is chosen, pick one: if
`alcohol-delivery-areas` is retired, the borough redirects must target
`/pages/alcohol-delivery` directly or they will chain.

Also note `alcohol-delivery` drew 11 sessions in 90 days and `alcohol-delivery-service`
drew 27, so `alcohol-delivery` is the weaker of the two as a consolidation target.

## 5. What the redirects got right

Most of the 749 fire correctly — the older gift, tequila and wine cleanups all point
from handles that no longer exist. That part of the job is sound.

## 6. Still outstanding: the internal-link fix

Separate from URL redirects. A fresh sample of 50 pages taken today still carries
**947 absolute internal links and 933 `www` references** — 47 of the 50 pages are
unchanged. The corrected bodies in `seo/internal-links/bulk/*.csv` have not been
imported. That work is still to do, and it is what stops internal links from
302/301-ing through the wrong host in the first place.
