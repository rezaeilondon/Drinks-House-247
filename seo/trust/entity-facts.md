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
| DPS | **deliberately not recorded here.** The owner asked for it to stay private, and a DPS name is not a ranking factor, so there is nothing to trade off. It belongs on the licence summary displayed at the premises, not on the website or in this repo. |

## Why this is on hold

The company was dissolved roughly twelve months ago and is mid-restoration. Publishing
company, VAT and licence credentials on pages whose entire purpose is to prove
legitimacy would mean publishing claims that may not currently be true.

Three things to confirm before any of it ships:

1. **Premises licence.** A premises licence lapses when the company holding it ceases to
   exist. Dissolution does that, and the window to file an interim authority notice is
   short. This needs Wandsworth Council licensing and a licensing solicitor — not an SEO
   decision. Selling alcohol without a valid licence is a criminal offence.
2. **VAT registration.** Dissolution normally triggers deregistration. Confirm 339765749
   is live with HMRC before it appears anywhere public.
3. **Restoration status.** Administrative restoration treats the company as having
   continued in existence as though never dissolved, which is what makes these
   credentials publishable again. Confirm it has completed.

Companies House could not be checked from this environment — the network egress proxy
blocks it — so everything above is as supplied by the owner and is unverified.

## What ships once restoration completes

- Licensing & compliance page (licence number, issuing council, Challenge 25)
- Company identity block in the footer and on `contact-us` (name, number, registered office)
- `Organization` JSON-LD carrying the company number and VAT number
- Challenge 21 → Challenge 25 upgrade, once the owner confirms the operational policy
