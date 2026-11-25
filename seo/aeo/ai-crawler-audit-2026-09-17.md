# How drinkshouse247.co.uk reads to AI crawlers — audit, 2026-09-17

## Scope and one hard limitation

**The live site could not be fetched from this session.** The egress proxy blocks
`drinkshouse247.co.uk` under this environment's network policy, and the proxy README is
explicit that a blocked host is reported rather than routed around. So everything below
comes from the Shopify Admin API — the theme source, the shop settings, the app config,
and the full text of 2,140 pages, articles and products.

That matters for one thing in particular: **the rendered `robots.txt` was not read.**
What was established instead is that the theme contains **no `templates/robots.txt.liquid`**,
so the store serves Shopify's stock robots.txt, which does not name or block AI crawlers.
Confirm by opening `drinkshouse247.co.uk/robots.txt` — if `GPTBot`, `ClaudeBot`,
`PerplexityBot`, `CCBot` or `Google-Extended` appear under a `Disallow: /`, nothing else
in this document matters until that is undone.

## What was found

### 1. The business entity was split across three identifiers

An `@id` is how a machine decides two mentions are the same organisation. The site was
using three, so the entity fragmented:

| `@id` | Where | Count |
|---|---|---|
| `…co.uk/#localbusiness` | page bodies | 42 |
| `…co.uk#business` (no slash) | page bodies | 5 |
| `…co.uk/#organization` | the trust pages built this week | 4 |

Plus **an anonymous `Organization` with no `@id` at all**, injected by the Smart SEO app
on *every* template via `snippets/smartseo.base.info.jsonld.liquid`. An anonymous node
cannot be merged with anything, so every page was asserting a business that could not be
tied to the business asserted next to it.

**Correcting something stated earlier in the session:** the 42 `@id`s are written with
the `www.` host, and I described that as pointing at a redirecting domain. It does not
reach the browser that way — `layout/theme.liquid` runs
`{{ content_for_layout2 | replace: 'www.drinkshouse247.co.uk', 'drinkshouse247.co.uk' }}`,
so those are rewritten to the apex host at render. The fragmentation is real; the www
part of it is not.

### 2. Two different sets of social accounts were published

`sameAs` is among the strongest identity signals available, and the site asserted both:

- Contact page: `instagram.com/drinks.house.247`, `x.com/drinks_house247`
- About page **and the Smart SEO app**: `instagram.com/drinkshouse247.co.uk`, `twitter.com/drinkshouse247`

Facebook agreed in both. **Owner confirmed 2026-09-17** that `@drinks.house.247` and
`@Drinks_House247` are the live accounts. The app settings metafield has been corrected,
which fixes `sameAs` on every page at once, and the About page now carries the same set.

### 3. Ten Recipe schemas were silently dead

`10-classic-cocktails-for-world-cocktail-day` carries ten `Recipe` blocks, every one
invalid for two compounding reasons: each is wrapped in `// <![CDATA[ … ]]>`, and each
`description` contains literal newlines inside a JSON string. Both are parse failures, so
all ten were being discarded. Repaired and validated — see `jsonld-repairs.csv`.

### 4. Smaller entity defects

- **`shop.name` is `"Drinks House 247 "`** — trailing space, and the app writes it into
  the `name` of the Organization on every page.
- **Billing address is malformed** for schema use: `city` is `"Battersea, london"`,
  `address1` is `"99-109 Lavender hill"`, `address2` is `"unit 95A"`. This is why
  `EnableStoreAddress` was deliberately **left off** — switching it on would publish
  `"addressLocality": "Battersea, london"` sitewide. Fix the address in Shopify admin
  first, then enable it. Not changed here: a billing address is a business record, not a
  marketing field.
- **`PriceRange` was `"$"`** on a UK business. Corrected to `"££"`.
- **Facebook URL carried `?modal=admin_todo_tour`**, an admin artifact. Stripped.

### 5. The theme defers nearly all JavaScript until human interaction

`layout/theme.liquid` rewrites `content_for_header` so scripts become
`type="lazyload_int"` with `data-src`, stylesheets become `data-href`, and a
`w3_loadscripts` class holds everything until `keydown`, `mousemove`, `touchmove`,
`touchstart`, `touchend` or `wheel` fires. A crawler does none of those.

**The main body text is safe** — `content_for_layout` is server-rendered, so the words on
the page are in the HTML. The exposure is images (`data-src` rather than `src`) and
anything an app injects through the header. Worth verifying against the rendered source
once the site can be fetched.

## What was changed

| Change | Where |
|---|---|
| About page rebuilt as the canonical entity page | `/pages/about-us` |
| `Organization` + `AboutPage` + `FAQPage` JSON-LD, one `@id` | `/pages/about-us` |
| Company number, VAT, premises licence in a facts table | `/pages/about-us` |
| Corrected `sameAs` sitewide | Smart SEO settings metafield |
| `priceRange` `$` → `££`; Facebook URL cleaned | Smart SEO settings metafield |
| 10 Recipe schemas repaired | `jsonld-repairs.csv` (pending import) |

The old About page also contradicted the rest of the site — "within 30 minutes" against
30–45 elsewhere, "open seven days a week" against 24/7 — and carried an unverifiable
"best prices" claim. All three are gone.

An earlier draft of the rebuilt page included `"foundingDate": "2018"`, inferred from the
company number falling in the range issued around April 2018. That is a guess, not a
checked fact, and it was removed before the page was finalised rather than published as
structured data.

## What is still worth doing

1. **Read `robots.txt`.** Highest value, thirty seconds, and it gates everything else.
2. **Consolidate the 47 remaining `@id`s** onto `…co.uk/#organization`. Same delivery
   problem as the Challenge 25 tail: it needs a bulk import, not 47 API round trips.
3. **Add `templates/robots.txt.liquid`** to name AI crawlers explicitly rather than
   relying on the default, and to declare the sitemap. Needs a theme write, which the
   MCP blocks for the live theme.
4. **Fix the store address and name** in Shopify admin, then switch `EnableStoreAddress`
   on so the app publishes a correct address sitewide.
5. **Consider an `llms.txt`.** Shopify has no root-file hosting, so it would have to be a
   page plus a redirect from `/llms.txt`, which 404s today and so would fire. A 301 to an
   HTML page is an imperfect substitute for a plain-text file — worth doing only after
   items 1 to 4.
