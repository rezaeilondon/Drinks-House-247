# Content reliability audit — 2026-09-16

Scanned all 2,142 resources (272 articles, 419 pages, 1,449 products) held on the store.
Ranked by how much damage each finding does if someone checks.

## 1. The DPS name is already published, 39 times

39 articles carry the byline **"By Javad Rezaei Zadeh, Drinks House 247"**.

On 16 September the owner asked for the DPS name to stay private, and it was kept out of
this repo and off the two new trust pages on that basis. It is already on the public site.
The owner needs to decide: leave it (a named author is a genuine E-E-A-T asset) or remove
it from all 39. Either is fine — but it should be a decision, not an oversight.

## 2. An expert-reviewer byline that needs verifying

Two articles carry **"Reviewed by Sarah Jenkins, ANutr, Registered Associate Nutritionist"**:

- `how-low-calorie-drinks-can-transform-your-party`
- `the-surprising-calorie-difference-vodka-soda-and-cola`

Elsewhere the copy asserts *Sommelier* (5), *WSET Level 3* (1) and *WSET* (1).

**If these people reviewed the articles, say more about them** — a bio, a photo, an AfN or
WSET registration number, a link. Verifiable credentials are worth a great deal.

**If they did not, the bylines have to come off.** A fabricated expert reviewer is exactly
what Google's spam policies target, ANutr is a registered designation held by real people
on the Association for Nutrition register, and a nutritionist byline on alcohol content
would not survive being checked. This is the single highest-risk item on the site.

## 3. Health and nutrition claims on alcoholic drinks

Retained Regulation 1924/2006 is strict here. Drinks over 1.2% ABV **must not carry health
claims at all**, and may carry nutrition claims only about low alcohol, reduced alcohol or
reduced energy.

That means the calorie angle itself is largely fine — "reduced energy" is a permitted
claim. These are not:

- `top-10-alcoholic-drinks-with-the-least-calories` (**1,454 sessions, the single
  biggest traffic source on the site**) — of a Bloody Mary: *"Packed with vitamin C,
  potassium and vitamin A, you can enjoy…"*. A nutrient claim on an alcoholic drink.
- `how-low-calorie-drinks-can-transform-your-party` — *"a fantastic way to promote
  healthier choices"*. A health claim.
- `can-black-tea-cure-your-hangover` (275 sessions) — *"any tea should help cure your
  hangover"*. A health claim about tea, and not well supported.
- `the-best-food-to-cure-a-hangover` — *"classic remedy"*, *"ability to rehydrate"*.

38 resources match the health-claim pattern in total. The fix is not to delete the
content: it is to strip the benefit framing and leave the factual calorie information,
which is both permitted and what people are actually searching for.

## 4. A comparative claim that is not verifiable

`specialist-alcohol-retailer-vs-supermarket-why-drinks-house-247-beats-waitrose-ms-tesco-every-time`

Naming competitors in a comparison is lawful in the UK, but the Business Protection from
Misleading Marketing Regulations 2008 require comparisons to be objective and to compare
verifiable features. *"Beats Waitrose, M&S & Tesco Every Time"* is a subjective
superiority claim in the title, the URL and the H1.

Rewrite around what is objectively true and checkable — 24-hour availability, delivery
inside 30–45 minutes, range depth — and drop "every time".

16 resources name competitor retailers. Separately, several gift guides recommend
Selfridges, Harrods, Fortnum & Mason, John Lewis and Bloom & Wild to your own readers.

## 5. Nine broken internal links

| Target | Links | Example source |
|---|---|---|
| `/pages/valentines-day-alcohol-delivery-london-uk-2026` | 3 | `champagne-chocolate-flowers-…-2026` |
| `/pages/send-tequila-as-a-gift-uk` | 2 | `best-tequila-gifts-uk-london-…-2026` |
| `/pages/tequila-gifts-for-him-uk` | 1 | same |
| `/pages/tequila-gifts-for-her-uk` | 1 | same |
| `/pages/tequila-birthday-gift-uk` | 1 | same |
| `/pages/happy-birthday-champagne` | 1 | `best-champagne-for-birthdays` |

Several of these have URL redirects pointing at `/`, so a reader does not hit a hard 404 —
they land on the homepage, which Google treats as a soft 404 and which strands the reader.

## 6. Checked and clear

- **Unsourced statistics: 2 only** (`personalised-moet-champagne-2026-gift-guide`,
  `send-flowers-and-champagne-the-ultimate-gift-guide-2026`). Much better than expected.
- **Stale years: a false alarm.** 69 resources mention 2023–2025, but nearly all are
  vintages in product names (Château Minuty 2024, Macallan Rare Cask 2023). Correct as is.
- **Excessive-drinking framing: 3 resources**, chiefly `top-12-easy-drinking-games`
  (650 sessions). Worth a read against CAP rule 18 on immoderate consumption, but it is
  not the systemic problem the volume of party content suggested it might be.

---

# Fixes applied — 2026-09-16

The owner could not vouch for who reviewed the content and asked for it to be fixed.
An unverifiable expert credential that the business owner himself cannot confirm is a
fabricated credential, so all of them came off.

## Fabricated experts removed (3 found, not 1)

The original audit caught one. Looking properly turned up two more:

| Name | Claim | Where |
|---|---|---|
| Sarah Jenkins | "ANutr, Registered Associate Nutritionist" reviewer byline | 2 articles |
| Jamie Collins | "Expert mixologist" with a direct quote | `the-surprising-calorie-difference-vodka-soda-and-cola` |
| Dr. Elaine Matthews | "nutrition expert at the London Institute of Public Health", direct quote | same article |

All three are gone.

## A fabricated credentials block

`premium-whiskey-cigar-gift-sets-london-…` claimed the author is "a certified spirits
specialist" holding "membership in the **Institute of Masters of Wine** and the UK Spirits
Academy". The IMW is real and polices the MW title; the UK Spirits Academy could not be
found. Replaced with what is verifiable: that he runs the business.

## Fabricated social proof on the same page

That page also carried:

- **Three invented customer testimonials** — "Charlotte M., London", "Thomas D., Finchley",
  "Emily R., Kensington", each with a full quote. Removed and replaced with a link to
  `/pages/reviews`, which is the position the whole reviews page argues for.
- **An invented case study** — a "Prestigious Financial Firm, Canary Wharf" corporate order.
  Removed.
- **An invented statistic** — "a 98.4% on-time delivery rate". Removed.
- **Five invented products with prices and dead order links** — "The Connoisseur's
  Collection … Price range: 350 - 450 … `/order/connoisseurs-collection`". None of the
  products or the `/order/*` URLs exist. One even read "Price range: 380 - 350", reversed.
  Replaced with links to the real whisky gifts and alcohol gift sets collections.
- **Overstated compliance claims** — digital government-ID verification at checkout and
  contactless electronic age checks on delivery. Replaced with the Challenge 21 policy
  that actually operates.
- Three dead links (`/luxury-cigars-london`, `/same-day-alcohol-delivery-london`,
  `/whiskey-gift-sets-london`) repointed at real collections, and a mangled temperature
  ("18-216C (64-706F)") corrected to 18–21°C (64–70°F).

## Health and nutrition claims

Reframed on the four traffic-bearing articles. The calorie information stays — reduced
energy is a permitted claim — the benefit framing does not:

- `top-10-alcoholic-drinks-with-the-least-calories` (1,454 sessions): "Packed with vitamin
  C, potassium and vitamin A" removed.
- `can-black-tea-cure-your-hangover` (275): rewritten to say plainly that no tea cures a
  hangover, that only time does, and that tea helps with rehydration and nothing more.
  Also removed advice to drink turmeric tea "to counteract the inflammatory effects of
  alcohol" before a night out.
- `how-low-calorie-drinks-can-transform-your-party`: "healthy alcoholic beverages",
  "guilt-free" and "promote healthier choices" removed throughout.
- `the-surprising-calorie-difference-vodka-soda-and-cola`: "supports health and weight
  management goals" replaced with a plain statement that fewer calories is the whole of
  the claim.
- `the-best-food-to-cure-a-hangover`: "classic remedy" framing on chicken soup removed.

## Broken links

Five of six fixed, all repointed to pages that exist. Still outstanding: one link to
`/pages/happy-birthday-champagne` in `best-champagne-for-birthdays`, which should go to
`/pages/celebrate-with-our-happy-birthday-champagne`.

## Still to do

1. **The DPS name.** 39 article bylines carry it. Still the owner's decision — it is a
   genuine E-E-A-T asset, and his instruction was to publish it where it helps ranking.
   A byline does; a licence page does not.
2. **Twelve more author bios** assert "over a decade of experience", "certified
   sommelier", "seasoned mixologist", "WSET". These are claims about the owner, so he can
   confirm or deny each. They were left alone rather than guessed at.
3. **The comparative page** still titled "Why Drinks House 247 Beats Waitrose, M&S & Tesco
   Every Time" — not objectively verifiable, needs a retitle and a handle change plus
   redirect.
4. **A full fabrication sweep.** Three invented experts, three invented testimonials, an
   invented case study, an invented statistic and five invented products all turned up in
   the handful of pages examined closely. That rate suggests more across the remaining
   2,100 resources.

---

# Fuller fabrication sweep — 2026-09-16

Scope: all 418 pages and 272 articles, pulled fresh, scanned for six defect classes —
attributed testimonials, quoted named experts, "case study" markers, self-performance
statistics, invented price lists, and dead internal links. Results below are what
survived manual verification; the raw regex hits were mostly noise (357 "precise
statistic" hits were ABV percentages, for instance).

## What was fixed, and where

### `unique-craft-beer-gift-baskets-for-every-occasion` (Page/703925911927)
- Dead `<a href="/order">` repointed to `/collections/beers`.
- "What Our Clients Say About Our Craft Beer Gift Hampers" — two paragraphs summarising
  reviews nobody can check ("Testimonials often mention…", "Many customers praise…")
  replaced with a link to `/pages/reviews`.
- **"curated craft beer gift baskets for thousands of satisfied UK customers"** removed.
  The store has taken 173 orders. Replaced with what is actually true: every basket is
  hand-packed to order.
- Two `www.` hosts in the LocalBusiness JSON-LD canonicalised to the apex domain.
- The I. Cabras (2017) micro-brewing citation was checked and **kept** — it is a real
  academic source, correctly attributed, and on-topic.

### `the-ultimate-guide-to-luxury-champagne-delivery-and-alcohol-gift-sets` (Page/704233406839)
- Three invented testimonials removed (2,558 bytes), attributed to "James R., Head of
  Operations, Financial Services Firm, Canary Wharf", "Charlotte B., Wedding Planner,
  Chelsea" and "Sophie M." — all unverifiable, and the kind of thing that fails a Google
  quality review outright.
- "Case Study: Large-Scale Corporate Gifting in The City" — an unnamed client, 50 bespoke
  orders, "zero substitutions", "has since exclusively partnered with us" — removed.
- Replaced with a short section pointing at `/pages/reviews`.
- Two `www.` JSON-LD hosts canonicalised.

### `personalised-moet-champagne-2026-gift-guide` (Page/702788501879)
- Invented anecdote removed ("One standout case involved a wedding party using bespoke
  Moët bottles as table centrepieces…").
- Unsourced statistic removed ("Survey data in the UK shows that over 70 percent of
  people recall receiving a customised gift long after the event").
- Two further unsourced survey appeals and one invented "average turnaround for
  personalised moet champagne is five days" removed.
- Invented corporate case study removed ("A case study from a London-based firm showed
  that custom-branded Moët bottles led to increased client retention").
- **Competitor promotion removed** (2,187 bytes): a four-row comparison table sending
  readers to Selfridges, John Lewis, Harrods and Farrar & Tanner, plus the paragraph
  calling them "trusted for quality and authenticity". Replaced with a buyer's checklist
  (who holds the licence, where stock is sourced, personalisation lead time, age
  verification at the door) that points back to `/pages/authenticity-and-sourcing`.
  The Moët official / Pharrell Williams Forbes link was kept — it is a real citation.
- A malformed heading — raw markdown link syntax leaked into the HTML as
  `<h2>[Drinks House 247: …] (https://drinkshouse247.co.uk)</h2>` — repaired.
- **`Article written using RankPill` credit removed**, along with its dofollow outbound
  link. Publishing a generator credit on a commercial page is a direct signal of
  unreviewed auto-generated content.
- Four `https://drinkshouse247.co.uk/ru/...` links — absolute, and pointing at the
  **Russian locale** of this UK site — made relative, and their `target="_blank"` stripped.

### `rare-vintage-champagne-delivery-london-fast-service` (Article/1023787270519)
- A verbatim academic thesis abstract on "strategic reengineering of e-commerce processes
  in the fashion-luxury industry" removed. It was dropped into a champagne delivery
  article with no connection to the subject.
- A second academic excerpt removed — a methodology note on last-mile delivery keyword
  layers (L. Cai, 2023), equally irrelevant.
- "Drinks House 247 Ltd offers tasting experiences and educational resources" removed. No
  such service exists. Replaced with the Challenge 25 age-verification policy, which does.

### `best-champagne-for-birthdays` (Article/1023806833015)
- `/pages/happy-birthday-champagne` repointed to
  `/pages/celebrate-with-our-happy-birthday-champagne`. This was the last live-broken
  internal link on the site.

## Checked and deliberately left alone

- **"Luc Mobihan, Chef, Restaurant Saint Placide, Saint-Malo"** on the Billecart-Salmon
  Blanc de Blancs product — verified as genuine producer marketing copy, not an invented
  endorsement.
- **The Lily Bollinger quote** — a real, widely documented quotation.
- **The I. Cabras (2017) craft brewing citation** — real and on-topic.
- **The twelve author-bio credential claims** ("certified sommelier", "WSET", "over a
  decade of experience") — the owner confirmed these are true, so they stay. They are an
  E-E-A-T asset; they would be stronger still with a certificate number or awarding body.

## Dead-link position after this sweep

18 internal links pointed at 15 distinct targets that returned nothing. Thirteen of those
targets were already resolved by existing redirects. The two genuinely broken ones —
`/pages/happy-birthday-champagne` and `/order` — are both fixed above. **Zero live-broken
internal links remain.**

## What this leaves outstanding

1. **The comparative page** `specialist-alcohol-retailer-vs-supermarket-why-drinks-house-247-beats-waitrose-ms-tesco-every-time`
   still needs a retitle, a handle change and a redirect. Under the Business Protection
   from Misleading Marketing Regulations 2008, comparative advertising has to be
   objectively verifiable; "beats … every time" is not.
2. **The bulk internal-link CSVs** (773 resources) still need importing.
3. **Eight inert redirects** — their source pages are still published, so Shopify never
   reaches the redirect. They need unpublishing first.
4. **Search Console impressions** before retiring any delivery page.
5. **Restoration confirmation** before any company number, VAT number or licence number
   is published.
