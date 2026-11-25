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

## Pages and articles fixed (all 81 targets reviewed)

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
| page | veuve-clicquot-on-special-occasions | Vintage 2012 → 2015, Vintage 2008 removed |
| page | send-a-bottle-of-champagne-as-a-gift | Vintage 2012 → 2015, Vintage 2008 removed |
| page | perfect-champagne-gift | Rich section showed the Rich Rosé image; vintage labels |
| page | food-pairing-veuve-clicquot | Rich section showed the Rich Rosé image; vintage labels |
| page | surprise-someone-with-veuve-clicquot | Glassware, champagne-bucket and personalisation claims; vintage labels |
| page | veuve-clicquot-champagne-gift-guide | Made-up delivery tiers replaced with the real rates. Glassware and personalisation claims, Rich image |
| page | veuve-clicquot-champagnes | Rich image, Vintage 2012 → 2015, Vintage 2008 removed |
| page | vintage-champagne-an-emotionally-engaging-journey-through-time | 2008 now links Krug 2008; 2012 now links La Grande Dame 2012 |
| page | christmas-alcohol-gift-guide | Links to draft products removed |
| page | champagne-for-engagement-gift-a-toast-to-celebrate-love | Draft-product links, vintage labels |
| page | delivery-anniversary-gifts-a-unique-way-to-celebrate | Fresh-fruit baskets, gift towers, baked goods and cheese claims removed (truffles linked instead). Empty heading, empty Instagram embed, keyword-stuffed spans and duplicate CTA removed |
| page | gifting-champagne-the-ultimate-guide-for-special-occasions | Brut Nature / Extra Brut described as fruitier (reversed); cash |
| page | red-wine-delivery | False partnership claim with 11 London restaurants and the outbound restaurant links removed. Pinot Grigio and Sauvignon Blanc described as reds. "Within 30 minutes", "order until midnight", "over 1,000 red wines", hashtags |
| page | send-a-gift-of-champagne | Bulk pricing and VAT invoicing claims removed; Challenge 25 wording (Pol Roger is stocked, so it stays) |
| page | champagne-cases-an-effervescent-journey-of-taste | Blanc de Blancs links pointed at the Blanc de Noirs collection |
| page | experience-the-joy-of-giving-with-champagne-gift-next-day-delivery | "Over 100 brands", mini spirits in gift sets, "on time, every time" |
| page | champagne-gift-basket-ideas | Temperature-controlled packaging and engraved-flute claims; "Veuve Clicquot" named as a prestige cuvée (now La Grande Dame) |
| page | wine-gifts | "489 wines" (now "more than 400"), Prestige Pearl price £390 → £380, FAQ price maths, "tracked" UK delivery |
| page | alcohol-delivery-as-a-gift | Macallan 12 anchor pointed at the whisky collection; "order before midnight" cut-off removed |
| page | late-night-wine-delivery-near-me | Checked; no change needed |

| page | champagne-gifts-birthday | Tequila photos (818, Clase Azul) captioned as champagne replaced with Piper-Heidsieck and Laurent-Perrier gift boxes. Unstocked Bollinger 2002 and Lanson replaced. Product photos now link to their products. Glassware section reworded |
| page | champagne-50th-birthday | Unstocked Perrier-Jouët Grand Brut and Nicolas Feuillatte replaced with Belle Epoque 2014 and Laurent-Perrier La Cuvée. "Grand Vintage 2013" (stock is 2015), "Louis Roederer Brut" (is Collection 243), Nectar Rosé (only the white is stocked) and Moët link pointing at Ice Impérial corrected. Krug, Ruinart, Charles Heidsieck and Billecart now link to products |
| page | a-heartfelt-gift-red-wine | Margaux labelled 2019; stock is 2021 |
| page | celebrating-champagne-the-ultimate-guide-to-styles-types-and-moments | "Non-vintage Champagnes" linked to a collection led by chocolate truffles; Rosé link moved to the Rosé Champagne collection |
| page | understanding-champagne-varieties-your-guide-to-selecting-the-best-bubbles | "Crème brülée" typo (3 places) |
| page | personalised-alcohol-gifts-the-ultimate-guide-to-gifting-spirits-wine | Rewritten. Engraving, custom-label and logo-branding services removed (not offered); AI images of engraved bottles removed; honest "Do you engrave? No" FAQ; birth-year vintages, gift message, truffles and gift sets instead |
| page | craft-beer-gift-sets-for-him-the-ultimate-guide | Rewritten as "Beer Gifts for Him" (URL unchanged, new title and SEO title/description). No craft beer gift sets are stocked; fake research quotes, invented customer reviews, subscriptions, branded glassware and engraving removed; built from real stock (BrewDog, Guinness, Madri, Peroni, Asahi) |
| page | personalised-moet-champagne-2026-gift-guide | Rewritten. Engraving and custom labels (not offered), advice to buy elsewhere, doubtful history (Oscars/Wimbledon partner, 1833 royal appointment, 1961 Oscars) and Saturday delivery removed; now built from the 15 Moët products stocked |
| page | champagne-bottle-size-guide-exclusive-selections-from-drinks-house-247 | Claimed to stock 9L, 12L and 15L bottles; none are stocked (largest is 6L). Reworded and links fixed |
| page | wine-as-a-christmas-gift-a-delightful-surprise | "Christmas Wine Deals" heading (no deals running) |
| page | alcohol-gifts-the-perfect-gesture-of-appreciation-and-celebration | Gin "gift sets with tasting notes and pairing suggestions" claim replaced with the gins actually stocked |
| article | late-night-beer-delivery-london | "Soft drinks" linked to a /ru/ product URL; implied chilled delivery |
| article | top-wine-gift-sets-to-buy-in-2026-from-budget-to-luxury | Engraved glasses / personalised labels line |
| article | personalised-champagne-box-guide-unique-gifting-ideas-2026 | Drinks House 247 section said it sells customisable and personalisable boxes; now says it doesn't engrave and lists what it does offer. Bottle-size link fixed |

Checked and left unchanged (no store-specific errors found): effortless-same-day-champagne-delivery page, dom-perignon-gift-set page, and the articles after-hours-liquor, alcoholic-beverage-delivery-guide, online-champagne guide, party-alcohol-calculator, dom-perignon-gift-review, large-format-wine-bottles, premium-wine-gift-trends, dom-perignon-delivery-london, corporate-champagne-gifts-london, dinner-party-cocktail-ideas, mothers-day-cocktails and the vodka soda calories article. Several of these describe industry features (tracking, subscriptions) in general, hedged terms rather than as Drinks House 247 services.

Flagged, not changed (as instructed): **veuve-clicquot-champagne-facts** article. Its history is wrong (it says Madame "Clicquat" opened a winery in Pouilly-sur-Loire in 1772, that Veuve Clicquot is 100% Chardonnay, and that Blanc de Blancs "contains no yeast"), it suggests sending champagne by Royal Mail, and it promises "15–30 minute delivery".

## Needs action in Shopify admin

- **Refund policy:** the API connection has no `write_legal_policies` scope, so this can't be done from here. In Settings → Policies → Refund policy, replace "Please note that returns will need to be sent to the following address: [INSERT RETURN ADDRESS]" with "For the address to send your return to, please ask a member of staff."

## Left for a decision

- **"Next-day UK" wording** appears about 310 times across pages. The store's published shipping rates are express 1–2 business days and standard 3–5 business days. This wording was left alone until there is a decision on whether next-day is offered.
- **Gift boxes on the wine-gifts page:** the page offers hand-tied presentation boxes (noir croc, ivory croc, blush velvet, chocolate) with photos, but no such product exists in the store. The wording was kept; confirm the service is real or remove it.
- **External images:** several blog articles still load AI images from Google Cloud and Supabase storage rather than Shopify. They work, but moving them to Shopify Files would be more robust.
- **PayPal and Apple Pay** are still mentioned. `supportedDigitalWallets` comes back empty from the API, so check that both are switched on at checkout.
