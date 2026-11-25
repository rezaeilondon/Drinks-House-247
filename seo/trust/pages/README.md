# Trust pages

Source of the live pages, so edits can be made here and re-applied rather than
reconstructed from the storefront.

| File | Live page | Created |
|---|---|---|
| `authenticity-and-sourcing.html` | `/pages/authenticity-and-sourcing` (Page/704647201143) | 2026-09-16 |
| `reviews.html` | `/pages/reviews` (Page/704647233911) | 2026-09-16 |

## Rules these pages were written under

- **No unverifiable claims about the supply chain.** Nothing about who we buy from,
  distributor relationships, or per-bottle inspection, because none of it could be
  confirmed. The authenticity page earns its keep on what a buyer can check themselves
  and what recourse they have, all of which is true and verifiable.
- **No invented testimonials.** The reviews page quotes nobody, and says plainly why.
- **No `AggregateRating` schema.** Google's structured-data guidance only permits
  aggregate rating markup for reviews a site collects and displays itself. Marking up a
  Google or Trustpilot score as our own is a rich-results violation and risks a manual
  action, so the page links to the live profiles instead.
- **No hardcoded rating or review count.** Product descriptions currently state "4.8 on
  Google · 223 reviews" on 245 products; that number will drift. The reviews page sends
  people to the live profiles, where the figure is always current.
- **Nothing that depends on the company restoration.** No licence number, no company
  number, no VAT number. Challenge 21 is named because that is the existing published
  policy; it becomes Challenge 25 only when the owner confirms the operational change.

## Sourcing claim — added 2026-09-16

The owner confirmed stock is bought from UK wholesalers holding AWRS (Alcohol Wholesaler
Registration Scheme) approval, naming Costco, DWG and Amathus among them. A
`Where our stock comes from` section now states the AWRS point, with a matching FAQ entry
in the visible copy and in the FAQPage schema.

**The named wholesalers were deliberately left off the page.** Naming your suppliers tells
competitors where you buy, names third parties publicly without their agreement, and adds
nothing the AWRS statement does not already carry. The load-bearing fact is the approval,
not the company names. Easy to add if the owner disagrees.

Two claims are still unconfirmed and still absent: whether orders are checked before
dispatch and by whom, and whether any brand-authorised retailer status applies.

## Footer links — added 2026-09-16

Both pages are in the `footer` menu (Menu/197081606), placed in the trust cluster:

    Home · All Products · Delivery Areas · About us · Reviews ·
    Authenticity & Sourcing · Challenge 21 · Job Opportunity ·
    Contact us · Blog · Sitemap · Your Privacy Choices

The **COVID-19 Delivery** item was removed in the same edit. It pointed at
`https://www.drinkshouse247.co.uk/pages/our-covid-19-delivery-policy` — a page unpublished
on 15 September, through the wrong host — so it was a broken link in the footer of every
page on the site.
