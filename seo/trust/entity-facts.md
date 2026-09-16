# Entity facts — HOLD, do not publish yet

Collected 2026-09-16 for the trust/credibility pages. **None of this is on the site**,
and none of it should go live until the company restoration completes.

| Field | Value |
|---|---|
| Registered name | Drinks House 247 Ltd |
| Company number | 11286226 |
| VAT number | 339765749 — **unverified, see below** |
| Trading address | 99–109 Lavender Hill, Battersea, London, SW11 5QL |
| Phone (already public) | 0203 488 3266 |
| Premises licence | **2022/320845** — holder: Drinks House 247 Ltd (11286226) |
| Licensed address | Unit 95a, Battersea Business Centre, 99–109 Lavender Hill, London SW11 5QL |
| Licence phone | 0203 393 8809 — **differs from the site's published number** |
| Authorised activity | Sale by retail of alcohol, **off supplies only** |
| Authorised hours | 00.00–00.00, all seven days (i.e. 24/7) |
| Public access | **None. "Premises not open to the public."** |
| DPS | **deliberately not recorded here.** The owner asked for it to stay private, and a DPS name is not a ranking factor, so there is nothing to trade off. It belongs on the licence summary displayed at the premises, not on the website or in this repo. |

## Why this is on hold

The company was dissolved roughly twelve months ago and is mid-restoration. Publishing
company, VAT and licence credentials on pages whose entire purpose is to prove
legitimacy would mean publishing claims that may not currently be true.

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

- **Phone.** The licence records 0203 393 8809. The website publishes 0203 488 3266 on
  every page and inside the LocalBusiness JSON-LD. Name/address/phone consistency is a
  local-search ranking input, and a licensing officer cross-checking the two would find a
  mismatch. Decide which is canonical and make both match.
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
