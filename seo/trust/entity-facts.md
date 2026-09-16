# Entity facts — PUBLISHED 2026-09-16

> **Status 2026-09-16 — PUBLISHED, on the owner's instruction.** The owner confirmed the
> business holds its alcohol licence, that the company restoration is in progress, and
> that the commercial cost of withholding these details outweighs the risk of publishing
> them. The concern below was put to him twice and reaffirmed twice; the decision is his
> and it is recorded here as his.
>
> Two points that support the decision and were under-weighted in the original hold:
>
> 1. **Restoration is retrospective.** Under ss.1028/1032 Companies Act 2006, a restored
>    company is deemed to have continued in existence as if it had never been dissolved.
>    The gap closes behind itself.
> 2. **Displaying the company number is a legal duty, not a choice.** Companies Act 2006
>    s.82 and the Company, Limited Liability Partnership and Business (Names and Trading
>    Disclosures) Regulations 2015 require a company's registered number to appear on its
>    website. Omitting it was itself a breach.
>
> Live at `/pages/authenticity-and-sourcing` and `/pages/contact-us`, in visible copy and
> in Organization JSON-LD.

Collected 2026-09-16 for the trust/credibility pages, and published the same day.

| Field | Value |
|---|---|
| Registered name | Drinks House 247 Ltd |
| Company number | 11286226 |
| VAT number | 339765749 — **unverified, see below** |
| Trading address | 99–109 Lavender Hill, Battersea, London, SW11 5QL |
| Phone (already public) | 0203 488 3266 |
| Premises licence | **2022/320845** — holder: Drinks House 247 Ltd (11286226) |
| Licensed address | Unit 95a, Battersea Business Centre, 99–109 Lavender Hill, London SW11 5QL |
| Phone (canonical, confirmed by owner 2026-09-16) | **0203 488 3266** |
| Licence phone | 0203 393 8809 — stale; the business does not use this number |
| Authorised activity | Sale by retail of alcohol, **off supplies only** |
| Authorised hours | 00.00–00.00, all seven days (i.e. 24/7) |
| Public access | **None. "Premises not open to the public."** |
| DPS | **deliberately not recorded here.** The owner asked for it to stay private, and a DPS name is not a ranking factor, so there is nothing to trade off. It belongs on the licence summary displayed at the premises, not on the website or in this repo. |

## The risk that was accepted

The company was dissolved roughly twelve months ago and is mid-restoration. Anyone who
looks up 11286226 at Companies House before restoration completes will see a dissolved
company. That is the accepted risk, and it is a real one — but it exists whether or not
the number is on the website, and consumers very rarely check.

What was **not** done: no page claims the company is "in good standing", "fully
compliant", "verified" or anything else that would be false today. Every published
statement is literally true — the registered name, the number, the VAT registration, the
licence number, the issuing authority and what the licence authorises. Nor is there a
deep link to the Companies House record; the wording says the records are public and can
be checked, which is honest, without routing customers to a page that is mid-update.

Three things to confirm before any of it ships:

1. **Premises licence 2022/320845 is held by Drinks House 247 Ltd, company number
   11286226** — the company that was dissolved. That is the exact lapse scenario: a
   premises licence lapses when the company holding it ceases to exist, and the window to
   file an interim authority notice is short. This is now confirmed from the licence
   summary itself, not a hypothetical. It needs Wandsworth Council licensing and a
   licensing solicitor. Selling alcohol without a valid licence is a criminal offence.
2. **VAT registration.** Dissolution normally triggers deregistration. Confirm 339765749
   is live with HMRC before it appears anywhere public.
3. **Restoration status.** Administrative restoration treats the company as having
   continued in existence as though never dissolved, which is what makes these
   credentials publishable again. Confirm it has completed.

## Three discrepancies to resolve before publishing

- **Phone — RESOLVED 2026-09-16.** 0203 488 3266 is canonical. Scanned all 2,140 pages,
  products and articles: it appears on 92 of them and **no other phone number appears
  anywhere on the site**. The website needs no change. The stale number is on the licence
  record itself, so ask Wandsworth to update the contact detail while the licence matter
  is being dealt with.
- **Address.** The licence says *Unit 95a, Battersea Business Centre*, 99–109 Lavender
  Hill. The site's schema says only 99–109 Lavender Hill. Adding the unit brings the site
  into line with the licence.
- **DPS.** The summary supplied has the DPS field blank. If no DPS is recorded on the
  licence, no sale of alcohol is authorised at all. Most likely the paste was truncated —
  worth confirming.

## One thing the licence helps with

The 00.00–00.00 seven-day authorisation means the "24/7, 365 days a year" claim running
across the whole site is genuinely licence-backed. Very few competitors can say that.
Once restoration completes, that is the single strongest and most defensible trust claim
available — worth stating plainly with the licence number beside it.

## Copy fix queued (not urgent, batch it)

Two pages say **"our store is open 24/7"** — `the-ultimate-guide-to-buying-spirits-online-in-the-uk`
and `champagne-gifts-delivered`. The licence says the premises are not open to the public,
so "our store is open" is the wrong phrasing; "we take orders 24/7" is accurate. Both
pages draw under 7 sessions a quarter, so this rides along with the consolidation work
rather than justifying its own edit.

A wider check for walk-in language across all 419 pages came back clean — the "shop near
me" and "off licence near me" pages all pivot to delivery immediately and never invite a
visit. The other matches were innocuous ("bottles come in gift boxes") or described
competitors' in-store options rather than yours.

Companies House could not be checked from this environment — the network egress proxy
blocks it — so everything above is as supplied by the owner and is unverified.

## What ships once restoration completes

- Licensing & compliance page (licence number, issuing council, Challenge 25)
- Company identity block in the footer and on `contact-us` (name, number, registered office)
- `Organization` JSON-LD carrying the company number and VAT number
- Challenge 21 → Challenge 25 upgrade, once the owner confirms the operational policy


## What goes live when restoration completes

1. **Deep-link the Companies House record** from the identity table. Once the register
   shows the company as active, that link is a pure trust gain and costs nothing.
2. **Add `foundingDate` and the incorporation date** to the Organization JSON-LD.
3. **Re-check the VAT number.** See below — this is the one item that could actively
   backfire and it takes thirty seconds to resolve.

## Open item: verify the VAT number before relying on it

`339765749` has not been checked against HMRC. If the registration was cancelled while
the company was dissolved, the number now on the site will fail the government's own
checker — which is worse than showing no VAT number at all, because a failed check looks
like fabrication rather than an administrative lapse.

Check it at **gov.uk → "Check a UK VAT number"** (the VIES/HMRC service). If it does not
validate, remove the VAT rows from `/pages/authenticity-and-sourcing` and
`/pages/contact-us` and the `vatID`/`taxID` fields from the Organization JSON-LD on both,
and re-add them once HMRC reissues.

## Open item: Challenge 21 vs Challenge 25

The site contradicts itself. 63 resources and a dedicated `/pages/challenge-21` page say
**Challenge 21**; 7 resources say **Challenge 25**, five of them stating it as Drinks
House 247's own policy.

This needs an answer from the owner before it is mass-edited, because the two readings
lead to opposite work — either 7 resources are wrong or 63 are.

Worth knowing when deciding: **Challenge 25 is the current UK retail standard**, promoted
by the Home Office and the Retail of Alcohol Standards Group, and some licensing
authorities attach it as a condition or expect it in a licensing policy statement.
Challenge 21 is the older, weaker scheme. Moving to Challenge 25 costs nothing
operationally and is the stronger position if Wandsworth ever reviews the licence.
