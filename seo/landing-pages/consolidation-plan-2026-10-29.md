# Page consolidation plan — 29 Oct 2026 (awaiting approval)

The store has 453 pages, 401 of them published, and many target the same search.
For example, there are 8 beer "near me" pages, 11 tequila-gift pages, 12 Veuve Clicquot
pages and 17 wine-gift pages. They compete with each other and with the collections.

This plan folds **151 published pages into 55 keepers**, leaving about 250 live pages.
The row-by-row list is in `consolidation-plan-2026-10-29.tsv`. Each row gives:

- the page to merge
- that page's word count
- where it will redirect
- the keeper's word count

## How each keeper was chosen

Search Console data was not available. The Supermetrics trial expired on 20 Aug 2026,
and the storefront is blocked from this environment. So the keeper in each group is the
page with the cleanest URL and the deepest content.

**Before approving, check Search Console → Performance → Pages.** If a page marked to
merge actually gets more clicks than its keeper, swap the two in that row.

## What happens to each merged page, once approved

1. Any unique, useful section (an FAQ or a local detail) is copied into the keeper.
2. The page is unpublished.
3. A 301 redirect is added from the merged page to its keeper.
4. Internal links are rewritten to point at the keeper. This covers pages, articles,
   collection descriptions, menus and `pages/html-sitemap`.

Rows that redirect to `/` are pages competing with the homepage for
"alcohol delivery London".

## Deliberately left alone

- **Area pages** (`alcohol-delivery-<area>`, 25 pages): genuine local intent.
- **Grape pages** (`<grape>-wine-delivery`).
- **Legal pages:** challenge-25, contact-us, reviews and the legal pages.
- **The "send gifts to London from <city>" set** (about 30 pages, roughly 400 words each,
  all on one template). These are the next-highest risk for Google's scaled-content
  signals. Review them after this round; most could become one "send gifts to London
  from abroad" page.
- **`job`** (62 words, still mentions COVID). Unpublish it or rewrite it; that is the
  owner's call.
