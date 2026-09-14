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

- **Answers hub page:** https://drinkshouse247.co.uk/pages/alcohol-delivery-london-questions-answered
  (Shopify Page ID `gid://shopify/Page/704641597815`) — 16 Q&As, two data tables,
  `LocalBusiness` + `WebPage` + `FAQPage` JSON-LD.
- **Blog:** handle `posts`, ID `gid://shopify/Blog/27034058814`.

## Daily posting — how it actually works

Articles are written ahead of time and queued using Shopify's own `publishDate`.
Shopify publishes each one on its date with no external automation involved.

**This replaced the Routine approach, which does not work on this account.**
Attaching a connector to a Routine was rejected twice with
`the connectors parameter is not available for this organization`, and a live test run
confirmed it: the fired session had no Shopify tools, stood down after 49 seconds, and
published nothing. The Routine (`trig_01PcHWoCiTDi11UkRkVSji3E`) is now **disabled** so it
does not fire pointlessly. Do not re-enable it unless connector support is confirmed —
verify by checking that `mcp_connections` on the trigger is non-empty, not by what any
settings screen displays.

### Queueing the next batch

1. Pick the next `"status": "pending"` entries from `backlog.json`, spreading clusters so
   several similar posts do not run back to back.
2. Write each article to the AEO template in `daily-post-playbook.md`.
3. Create it with `articleCreate` on blog `gid://shopify/Blog/27034058814`, setting
   **`publishDate` to the target date and omitting `isPublished` entirely**.
   Setting `isPublished: true` alongside a future `publishDate` is rejected with
   `INVALID_PUBLISH_DATE`.
4. Confirm the response shows `isPublished: false` with the future `publishedAt` — that is
   what a correctly scheduled article looks like.
5. Mark the backlog entry `"scheduled"`, fill `published_at` and `article_handle`, add a row
   to `published-log.md`, then commit and push.

### Current queue

Seven articles are scheduled for 15–21 September 2026, one per day at 08:00 UTC.
70 topics remain pending. See `published-log.md` for the live list.

Top the queue up before it runs dry — there is no automation to do it for you now.
