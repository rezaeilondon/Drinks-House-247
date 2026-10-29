# Site health fixes — 23–29 Oct 2026

## Live now (store data)

- **Challenge 21 → Challenge 25** on 5 product descriptions and 4 FAQ metafields
  (`dh247.desc_sec1`):
  - dom-perignon-champagne-2013
  - dom-perignon-x-damien-hirst-vintage-2018-champagne-75cl
  - dom-perignon-x-damien-hirst-rose-2010-champagne-75cl
  - the-hirst-prestige-hamper
  - the-kaleidoscope-rose-hamper
- **7 two-hop redirect chains now go straight to their destination:**
  - champagne-delivered-uk → /collections/champagne
  - champagne-delivery-in-uk → /collections/champagne
  - champagne-delivery-uk-bringing-elegance-to-your-doorstep → /collections/champagne
  - online-champagne-delivery-1 → /collections/champagne
  - champagne-gift-next-day-delivery-effortless-celebrations → /collections/champagne-gifts
  - wine-home-delivered-same-day-wine-delivery-across-the-uk → /collections/wines
  - /same-day-alcohol-delivery-london → /
- **7 empty collections hidden from search and the sitemap** (`seo.hidden = 1`):
  doux-champagne, practicing-biodynamic-wines, carbon-neutral-wines,
  sparkling-red-wine, viognier, torrontes, sardinia.

## Draft theme: "SEO fixes 28 Oct (draft from live)"

Theme id 194077327735. **Preview it, then publish it from Online Store → Themes.**
Shopify blocks API writes to the live theme, so these changes can only go live this way.

- **Homepage heading:** the hidden H1 is gone. The visible about-section headline is now
  the page's single H1 and keeps its previous look.
- **Hero slide (the main homepage image):**
  - It loads immediately at high priority, as one responsive picture.
  - Before, it was lazy-loaded and then swapped for the full-size original.
  - The stale preload of slide 2 (banner01, from 2022) has been removed.
- **Text wrapping:** `body.page p { word-break: break-all }` no longer splits words
  mid-word on content pages.
- **Homepage delivery block:**
  - "Order below or Call" is now "Order online below".
  - "Free Delivery Available" is removed.
- **Footer:** the QeRetail credit link now has `rel="nofollow noopener"`.

The draft is a copy of the live theme as of 28 Oct, 23:5x UTC. If anyone edits the live
theme before the draft is published, repeat those edits on the draft first.
