# Content fixes — 1 October 2026

This records the content problems fixed on live pages and blog articles after the internal-link work. Every change was pushed through the Shopify Admin API one page at a time. Each body was read back and compared with the intended version before moving on.

The store policies were not touched, except for one flagged change that has to be made in the admin (see "Needs action in Shopify admin").

## Facts checked against the store before editing

| Claim on pages | What the store shows | Fix applied |
|---|---|---|
| "Challenge 21" | The policy page is `/pages/challenge-25` | Changed to Challenge 25 / "look under 25" |
| "Cash on delivery" / `"paymentAccepted": "Cash, …"` | Payment is taken at checkout | Removed cash; card, PayPal, Apple Pay and Google Pay wording left as it was |
| "Within 30 minutes" / "15–45 minutes" | The standard promise is 30–45 minutes inside the M25 | Changed to 30–45 minutes |
| Phone shown as `0203 488 3266`, `+44 0203…`, `at0203` | 020 3488 3266 | Normalised |
| Veuve Clicquot "Vintage 2012" | No such product. Every link goes to `veuve-clicquot-vintage-champagne-2015`. Vintage Rosé 2012 is a draft | Relabelled to Vintage 2015 and swapped the Vintage Rosé 2012 image (La Grande Dame 2012 is a real product and was left alone) |
| Veuve Clicquot Vintage 2008 | `veuve-clicquot-2008` is a draft, so the link returns a 404 | Removed from product lists |
| Cigar gift sets (Cohiba, Montecristo, Davidoff) | All tobacco products are archived; no cigars are sold | Page reframed as whisky gifts with cigar-pairing advice, plus a "Do you sell cigars? No" FAQ |
| Engraving, custom labels, branded or logo packaging, subscriptions, real-time tracking, temperature-controlled transport | No such products or services | Removed; replaced with gift message at checkout, or "contact us" for larger orders |
| "First order discount" | Only affiliate codes and EASTERVIP10 are active | Removed |
| Northern Ireland and Saturday delivery | Not offered (couriers serve the UK mainland) | Removed |
| "Belgian chocolates" in wine gift sets | Charbonnel et Walker truffles are sold separately | Reworded to suggest adding truffles to the order |
| Strongbow "Dark Fruit" link to `strongbow-original-cider` | That product handle is titled Strongbow Dark Fruit Cider | No change needed (false alarm) |
| Ruinart Rosé link to `ruinart-blanc-de-blancs-champagne-1` | That handle is titled Ruinart Rosé Champagne | No change needed (false alarm) |

## Pages and articles fixed (31 so far)

| Type | Handle | Main fixes |
|---|---|---|
| article | alcohol-delivery-3am-london | Licensing Act wording, Challenge 25, phone number |
| article | alcohol-delivery-to-office-london | Challenge 25 |
| article | craft-beer-delivery-in-london-fast-30-45-minute-delivery | Garbled research quote removed. Subscription, label, branded-box, tracking and temperature-control claims removed. Anchors and phone fixed |
| article | eco-friendly-sustainable-alcohol-brands-uk-the-complete-guide | Corrupted £ prices removed |
| article | 9-best-flowers-and-champagne-delivery-options-for-2026 | 8 competitor listings (with outbound links and prices) replaced with our own rose-and-champagne pairings. Retitled to "Flowers and Champagne Delivery in 2026: Best Pairings and How to Choose" with new SEO title and description (URL unchanged). Unsourced 30% stat, RankPill footer and empty heading removed |
| article | luxury-alcohol-gift-hampers-the-best-picks-for-christmas-special-occasions | Stale price column, competitor links, off-topic East Asia quote and engraving section removed. Branded-packaging claims softened. Anchors and phone fixed |
| article | notting-hill-carnival-drinks-guide | Missing apostrophes, Challenge 25, cases link |
| article | oktoberfest-at-home-beers-steins-and-snacks | Date wording, beer range link, Challenge 25 |
| page | 24-hour-alcohol-delivery-service | ChatGPT/AIPRM wrapper markup removed. Third-person wording, cash, pre-order and returns claims fixed |
| page | alcohol-gift-delivery-in-london-uk-perfect-for-celebrations | Truncated JSON-LD @id, cash on delivery, phone, Challenge 25 |
| page | alcohol-gift-sets-the-ultimate-guide-to-premium-drinks-gifts-in-the-uk | Garbled quotes, physical-store claim, engraving claims |
| page | best-beer-delivery-london | Challenge 25, cash, phone |
| page | booze-delivery-near-me | Wrong anchors (a Pinot Grigio, Captain Morgan and Prosecco product), missing spaces, "within 30 minutes", cash, Challenge 25, UK delivery times |
| page | champagne-shop-near-me | Vintage 2012 → 2015 |
| page | champagne-types | AIPRM markup. Blanc de Blancs and Non-Vintage links retargeted. Tasting-set claim |
| page | cost-of-veuve-clicquot | Vintage 2012 → 2015, Vintage 2008 removed |
| page | dom-perignon-champagne | AIPRM markup, "Benedictine Abbey" wording, P2 image, Lady Gaga image (draft product), empty headings |
| page | engagement-party-alcohol-delivery-… | Pasted HTML document unwrapped (fixes the broken CSS comment), service claims |
| page | office-party-alcohol-delivery-uk-… | Unwrapped. Net 30, bulk discounts, neutral packaging and free delivery claims removed |
| page | christmas-alcohol-gifts-delivery-… | Unwrapped. "Christmas 2025" and engraved-glasses claims |
| page | next-day-veuve-clicquot-champagne | Vintage 2012 → 2015, Vintage 2008 removed |
| page | premium-whiskey-cigar-gift-sets-london-… | No cigars sold; engraving, tracking and logo-packaging claims removed; Challenge 25; cash |
| page | prosecco-gifts-the-best-bottles-… | Duplicated, garbled serving block. DOCG typos, phone, lost dash |
| page | send-a-champagne-gift | La Grande Dame 2012 now links to its own product. Moët anchor fixed. Duplicated span text, empty headings, run-on headings, cash |
| page | send-gift-uk | Vintage 2012 → 2015 |
| page | veuve-clicquot-delivered-today | AIPRM markup, delivery-app mention, vegan claim, hashtags, Vintage 2012 |
| page | veuve-clicquot-gift-set-a-perfect-class-apart | Vintage 2012 → 2015, Vintage 2008 removed |
| page | veuve-clicquot-gifts | Vintage 2012 → 2015, "15–45 minutes" → 30–45, "Drinks House 24/7" → 247 |
| page | whisky-tasting-guide-for-beginners-… | Pasted HTML document unwrapped. Speyside claim, CTA links, email |
| page | wine-in-gift-boxes-the-perfect-present-for-any-occasion | Three duplicated sections and empty `<h1>` removed. "Happy customers", chocolates and next-working-day wording fixed, cash |
| page | wine-home-delivered-same-day-wine-delivery-across-london | Northern Ireland, Saturday delivery and first-order discount claims removed. Empty link, missing spaces, cash |

## Needs action in Shopify admin

- **Refund policy:** the API connection has no `write_legal_policies` scope, so this can't be done from here. In Settings → Policies → Refund policy, replace "Please note that returns will need to be sent to the following address: [INSERT RETURN ADDRESS]" with "For the address to send your return to, please ask a member of staff."

## Left for a decision

- **"Next-day UK" wording** appears about 310 times across pages. The store's published shipping rates are express 1–2 business days and standard 3–5 business days. This wording was left alone until there is a decision on whether next-day is offered.
- **PayPal and Apple Pay** are still mentioned. `supportedDigitalWallets` comes back empty from the API, so check that both are switched on at checkout.
