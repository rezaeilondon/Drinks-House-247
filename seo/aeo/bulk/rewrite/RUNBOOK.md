# Product description rewrite — unattended runbook

Everything needed to resume this job lives in this directory. A session that has
never seen the work before can pick it up from a cold start with no other context.

## What the job does

1,248 of 1,258 active products carry a `<style>` block at the **start** of
`descriptionHtml`. The `llms.txt` generator strips HTML tags but keeps the *text*
inside `<style>`, then truncates at ~300 characters — so every product's entry for
LLM crawlers is 300 characters of CSS and nothing else. The same field feeds
`/products/{handle}.json`, the UCP catalog search and Google Merchant Center.

The rewrite, per product:

1. Delete the hand-written `<script type="application/ld+json">` Product block.
   It is already stripped at render by `snippets/dh247-clean-description.liquid`,
   but feeds still read it, and 15 products state a price contradicting the live one.
2. Move the `<style>` block from the start to the **end** of the field.

Nothing else changes. The rendering is identical — CSS position inside the field
does not affect the cascade, and `@import` stays first within its own block, so it
stays valid. What changes is the first 300 characters a crawler sees: prose instead
of CSS. Prose already present is good (826 chars shortest, 1,836 median).

`verify.py` re-proves this per product: visible prose byte-identical before and
after, every `<style>` block surviving verbatim. Run it before a run; 0 failures
is the gate.

## State

| File | What it is |
|---|---|
| `plan.json.gz` | `{product_gid: {handle, title, old, new}}` for all 1,248 |
| `order.json` | Priority order — the 212 products in `llms.txt` first |
| `done.json` | Product gids already applied. **The resume pointer.** |
| `originals.json.gz` | Every original `descriptionHtml`, for rollback |
| `pending.json` | The batch `next.py` last emitted (transient) |

## The loop

```bash
cd seo/aeo/bulk/rewrite
python3 next.py 11000          # emits one GraphQL document, ~2 products
# -> send that document VERBATIM to the Shopify Admin API (graphql_mutation)
# -> confirm every userErrors array came back empty
python3 commit.py              # only now does done.json advance
cp done.json ../description-fix-progress.json
cd ../../.. && git add -A seo/aeo/bulk/ && git commit -q -m "Description rewrite progress: N/1248" && git push origin claude/shopify-store-connection-i6syn7
```

Repeat until `next.py` prints `ALL DONE`.

### Why the batch is small

The mutation text has to pass through the model's output, and batches over
~30 KB get truncated by the harness rather than shown. 11,000 bytes ≈ 2 products
is the tested working size. Raising it risks a silently truncated mutation.

### Why `commit.py` is separate

`done.json` advances only after a mutation has returned clean. An interrupt
between the two leaves the state consistent — the same batch is simply re-emitted
on the next run. Nothing is ever half-applied.

## Rules

- `productUpdate` with `descriptionHtml` **alone** is safe: `seo.title`,
  `seo.description`, tags, vendor, productType and status are all left intact
  (canary-verified). Do **not** add `seo:{description}` to the same mutation —
  passing a partial `seo` input nulls `seo.title`.
- `bulkOperationRunMutation` is blocked by policy. Do not try to route around it.
- Transcribe the emitted document verbatim. Do not regenerate, reformat or
  re-escape it.
- If a mutation returns a non-empty `userErrors`, stop and report it. Do not run
  `commit.py`.

## Rollback

```python
import gzip, json
orig = json.load(gzip.open("originals.json.gz", "rt", encoding="utf-8"))
# orig[product_gid] is the exact descriptionHtml before the rewrite
```
