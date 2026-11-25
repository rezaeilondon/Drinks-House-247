#!/usr/bin/env python3
"""Remove hand-written Product JSON-LD from product descriptions.

Why: every affected product page carries TWO Product entities. One is written by
hand into the description with a hardcoded price and a hardcoded
"availability": "InStock". The other is generated per-request by the Smart SEO app
(snippets/smartseo.product.jsonld.liquid) from `variant.price` and
`variant.available`, one Offer per variant, with sku/mpn/gtin/weight.

The app's version is strictly better and cannot go stale. The hand-written one
drifts the moment a price changes, and 18 products had already drifted by up to
£85. Updating the numbers would only reset the clock; deleting the block fixes it
permanently.

Only blocks that parse as JSON AND declare "@type": "Product" are removed. A block
that fails to parse, or declares anything else (FAQPage, Recipe, Article), is left
exactly where it is.
"""
import json, re

SCRIPT = re.compile(r'<script type="application/ld\+json">(.*?)</script>\s*', re.S)


def strip(html):
    """Return (new_html, removed_count, kept_count)."""
    removed = kept = 0

    def repl(m):
        nonlocal removed, kept
        try:
            obj = json.loads(m.group(1).strip())
        except Exception:
            kept += 1
            return m.group(0)          # unparseable: never touch it
        if isinstance(obj, dict) and obj.get('@type') == 'Product':
            removed += 1
            return ''
        kept += 1
        return m.group(0)

    return SCRIPT.sub(repl, html), removed, kept
