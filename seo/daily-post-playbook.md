# Daily Blog Post Playbook — Drinks House 247

This file is the complete instruction set for the daily automated post. The scheduled job
starts from a **fresh session with no memory**, so everything it needs is written down here.

---

## 0. Store facts (use these; do not invent others)

| Fact | Value |
|---|---|
| Business | Drinks House 247 |
| Site | https://drinkshouse247.co.uk |
| **Canonical host** | **Apex, no `www`.** This is the property in Google Search Console and the primary domain in Shopify. Never write `www.` into a link, a canonical, or JSON-LD. |
| Blog | handle `posts`, ID `gid://shopify/Blog/27034058814` |
| London delivery | 24/7/365, typically **30–45 minutes**, inside the M25 |
| UK delivery | Next day, UK mainland |
| Base | Battersea, London |
| Age policy | **Challenge 21** — recipient must be 18+, ID may be requested |
| Phone | 0203 4883266 |
| Email | sales@drinkshouse247.co.uk |
| Currency | GBP |

**Never state a product price, a stock level, or a delivery fee as fact.** Prices and stock
change daily. Link to the collection and let the live page show the price.

---

## 1. Pick the topic

1. Read `seo/backlog.json`.
2. Take the **first** entry with `"status": "pending"`. Prefer one whose cluster has not
   been used in the last 3 days, so the blog does not run six brand comparisons in a row.
3. If fewer than 10 pending entries remain, append 20 new ones following the gap
   framework in `seo/keyword-gap-analysis.md` before continuing.
4. Confirm the topic is not already covered: the store has 263 existing articles and 418
   pages. Query the Admin API for near-duplicate titles before writing. If it duplicates,
   mark that entry `"status": "skipped-duplicate"` and take the next.

---

## 2. Write the article — the AEO template

The entire point of this programme is to be **quotable by AI search** (ChatGPT, Perplexity,
Google AI Overviews, Copilot) as well as rank in Google. That requires a specific shape:

### Required structure

1. **`<h1>`** — the working title, phrased as the question wherever natural.
2. **Direct answer block, first.** A `<p>` of **40–60 words** that fully answers the
   question before any selling. This is the block an LLM lifts. It must stand alone and
   make sense quoted out of context — so name the business inside it, e.g.
   *"Drinks House 247 delivers across London 24 hours a day…"*.
3. **`<h2>` sections** that each answer one sub-question. Use question-shaped headings —
   they map to the follow-up queries models generate.
4. **At least one `<table>`.** Models lift tables near-verbatim. Comparisons, quantity
   maths, size charts, price bands, timings — whatever the topic supports.
5. **Specifics, not adjectives.** Times, volumes, temperatures in °C, UK units, ABV,
   ageing minimums. Checkable facts are what earn citations. "Premium quality service"
   earns nothing.
6. **FAQ section** — an `<h2>Frequently asked questions</h2>` with 3–5 `<h3>` questions,
   each answered in 1–3 sentences. Must match the JSON-LD exactly (see §3).
7. **Closing CTA** — one short paragraph with a link to the most relevant collection.
8. **Responsible-drinking line** where the topic touches quantity, parties or late-night
   ordering: note the Challenge 21 policy and that deliveries are to over-18s only.

### Length
900–1,400 words. Long enough to be substantive, short enough to stay dense. Do not pad.

### Voice
Match the existing house style: British English, plain and confident, second person,
no exclamation marks, no "unlock"/"elevate"/"dive into"/"in today's fast-paced world".
Read 2–3 recent articles from the blog before writing to match tone.

### Honesty rules (non-negotiable)
- Be even-handed in comparisons. If a cheaper bottle is the better buy, say so — that
  candour is exactly what gets a page cited rather than dismissed as marketing.
- No health claims. Do not imply any alcoholic drink is healthy, low-calorie as a benefit,
  or safer than another.
- No invented awards, scores, review quotes, statistics or customer testimonials.
- No competitor claims that cannot be verified. Comparisons stay factual and neutral.
- Never target or appeal to under-18s.

### Internal linking
Use the `internal_links` from the backlog entry, plus 2–4 more you verify exist. Link with
descriptive anchor text, never "click here". **Verify every URL** against the live store
before publishing — a 404 in a published article is worse than no link.

---

## 3. Structured data (JSON-LD) — required

Append a `<script type="application/ld+json">` block at the end of the article body
containing a `@graph` with:

- **`FAQPage`** — every Q&A from the FAQ section, matching the visible text word for word.
  Mismatched schema is a Google structured-data violation.
- **`Article`** — `headline`, `description`, `datePublished`, `author` and `publisher`
  (Drinks House 247).

Where the topic is London delivery logistics, also include **`LocalBusiness`** with
`areaServed: London`, the phone number, and `openingHours` of `Mo-Su 00:00-23:59`.

Validate the JSON parses before publishing. Malformed JSON-LD is silently ignored by
crawlers, which wastes the whole exercise.

---

## 4. Publish

Use `articleCreate` on blog `gid://shopify/Blog/27034058814`:

```graphql
mutation CreateArticle($article: ArticleCreateInput!) {
  articleCreate(article: $article) {
    article { id title handle publishedAt }
    userErrors { field message }
  }
}
```

Variables:

```json
{
  "article": {
    "blogId": "gid://shopify/Blog/27034058814",
    "title": "<working_title>",
    "handle": "<kebab-case, <=70 chars, contains the primary keyword>",
    "body": "<the HTML article including the JSON-LD script>",
    "summary": "<140-160 char plain-text summary = the direct answer, trimmed>",
    "author": { "name": "Drinks House 247" },
    "tags": ["<cluster>", "<2-3 topical tags matching existing blog tags>"],
    "isPublished": true,
    "metafields": [
      { "namespace": "global", "key": "title_tag",
        "type": "single_line_text_field",
        "value": "<=60 chars, primary keyword first, ends '| Drinks House 247' if it fits>" },
      { "namespace": "global", "key": "description_tag",
        "type": "single_line_text_field",
        "value": "<=155 chars, leads with the direct answer, not with the brand>" }
    ]
  }
}
```

Always follow the Shopify GraphQL workflow: `graphql_schema` → build →
`validate_graphql_codeblocks` → `graphql_mutation`. Check `userErrors` is empty; if it is
not, fix and retry rather than reporting success.

---

## 5. Record it

After a successful publish, in the repo on branch `claude/shopify-store-connection-i6syn7`:

1. Set that backlog entry's `status` to `"published"`, and fill `published_at` (ISO date)
   and `article_handle`.
2. Append one line to `seo/published-log.md`: date, title, target question, article URL.
3. Commit as `seo: daily post — <title>` and push with `git push -u origin claude/shopify-store-connection-i6syn7`.

If the push fails on a network error, retry up to 4 times with 2s/4s/8s/16s backoff.

---

## 6. Stop conditions

- **Never publish two articles in one day.** Check `seo/published-log.md` first; if today's
  date is already logged, stop and do nothing.
- If the Shopify connection fails, stop without publishing and leave the backlog untouched.
- If `userErrors` comes back non-empty twice in a row, stop and leave the entry pending.
