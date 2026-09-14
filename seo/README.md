# SEO programme — Drinks House 247

## What is here

| File | Purpose |
|---|---|
| `keyword-gap-analysis.md` | Which keyword clusters are saturated and where the real gaps are |
| `backlog.json` | The queue of topics for the daily post (77 pending at setup) |
| `daily-post-playbook.md` | Full spec the daily automation follows |
| `published-log.md` | One row per published post |
| `landing-pages/build-answers-hub.py` | Generator for the answers hub page (keeps visible FAQ and JSON-LD in sync) |
| `landing-pages/answers-hub.published.html` | Exact body published to the live page |

## Live assets

- **Answers hub page:** https://www.drinkshouse247.co.uk/pages/alcohol-delivery-london-questions-answered
  (Shopify Page ID `gid://shopify/Page/704641597815`) — 16 Q&As, two data tables,
  `LocalBusiness` + `WebPage` + `FAQPage` JSON-LD.
- **Blog:** handle `posts`, ID `gid://shopify/Blog/27034058814`.

## ⚠️ Daily automation — one manual step outstanding

A Routine was created that fires daily at **08:00 UTC**:

- Name: *Drinks House 247 — daily SEO blog post*
- Trigger ID: `trig_01PcHWoCiTDi11UkRkVSji3E`

**It currently has no Shopify connector attached** (`mcp_connections: []`), because this
organisation does not allow connectors to be attached to a Routine via the API. Until that
is fixed the daily session will start, read this repo, and then be unable to publish.

**To fix (one-time, ~1 minute):** open the Routine at
<https://claude.ai/settings/routines>, edit *Drinks House 247 — daily SEO blog post*, and
enable the **Shopify** connector for it. The prompt itself is already correct — do not
change it.

Alternatively, delete that Routine and recreate it from the same screen, pasting the prompt
stored on the trigger, with the Shopify connector switched on.

### Verifying it works
After the first run, check that `published-log.md` has a new row and that the article
appears at `/blogs/posts`. If the log is empty the morning after, the connector step above
has not taken effect.

## Regenerating the answers hub

```bash
python3 seo/landing-pages/build-answers-hub.py   # writes /tmp/landing_body.html
```
Then push the body to the live page with `pageUpdate` on page ID `704641597815`.
The script derives the JSON-LD FAQ text from the visible answers, so the two can never
drift apart — always edit the script, never the published HTML directly.
