# Internal linking audit

## What the data changed

Traffic was pulled from Shopify (ShopifyQL, sessions by landing page, 90 days) rather than
assumed. Two findings reshaped this work:

**1. The 418 SEO pages are not where the traffic is.**

| Type | URLs in top 100 | Sessions | Share |
|---|---|---|---|
| Blog articles | 26 | 6,490 | 46% |
| Products | 25 | 3,537 | 25% |
| System (`/`, `/cart`, `/search`) | 4 | 2,211 | 16% |
| Collections | 8 | 1,266 | 9% |
| **Pages** | **6** | **680** | **5%** |

Only six of the 418 pages appear in the top 100 at all. Blog articles carry nine times the
traffic that pages do. Effort belongs on articles and collections.

**2. Almost half of all sessions are on localised URLs.**

6,861 of 14,184 sessions (48%) land on `/ar/`, `/ru/` or `/zh/`. The single biggest content
page on the site is `/ar/blogs/posts/top-10-alcoholic-drinks-with-the-least-calories`.
These are not a side channel — they are half the business's organic traffic.

## The actual defect

Top articles are **already well linked**: contextual collection links, a tailored CTA
paragraph and a styled product grid. Adding more links would have been busywork.

The real bug is the *form* of the links. Many were written as absolute URLs:

```html
<a href="https://drinkshouse247.co.uk/collections/vodka">vodka</a>   <!-- breaks locale -->
<a href="/collections/vodka">vodka</a>                                    <!-- keeps locale -->
```

On a localised page, a relative link resolves within the locale — an Arabic reader on
`/ar/blogs/posts/...` following `/collections/vodka` lands on `/ar/collections/vodka`.
An **absolute** link throws them out of Arabic and back to the English site. With 48% of
sessions on localised URLs, this silently dumps a large share of readers out of their own
language mid-journey, and leaks link equity to a `www` host that is not the store's
primary domain (`drinkshouse247.co.uk`, apex).

## The fix

Convert absolute internal URLs to relative in article bodies, and add a contextual link to
the answers hub where it earns its place. Deterministic, low risk, no content rewriting.

## Checked and found NOT broken

- `/products/smirnof` (one `f`) — a real, active product, not a typo. Left alone.
- `/products/belvedere` — real and active.
- Hardcoded prices in product grids — all eight verified against the live catalogue and
  **currently correct**. They are a staleness risk over time, not a present defect.
  Revisit if prices change; consider replacing with links that carry no price.

## Progress

Tracked in `progress.json`. Work top-down by sessions, prioritising resources with
localised traffic, since that is where absolute links do real damage.
