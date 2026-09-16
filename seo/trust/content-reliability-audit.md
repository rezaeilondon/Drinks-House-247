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
