#!/usr/bin/env python3
"""Build a complete llms.txt for Drinks House 247.

The file Smart SEO publishes at /llms.txt is a 1.4KB stub, and the 158KB
template it also writes into the theme is never served -- Shopify does not
route arbitrary template names, which is why the app ships a URL redirect to a
CDN-hosted file instead. This script regenerates that CDN file's content in
full, from live Admin API data, so every published product, collection, page
and article is visible to LLM crawlers rather than a fraction of them.

Inputs (all produced by the catalog pull, see README.md):
  cat/products.json   live product data, keyed by product gid
  cat/tax_all.json    collections, pages, blogs+articles
  ../bulk/rewrite/plan.json.gz   cleaned descriptionHtml per product

Descriptions come from the rewrite plan where one exists, because those have
the <style> block moved out of the opening 300 characters. The prose itself is
byte-identical to what is live today -- only the CSS position differs -- so the
catalog is accurate whether or not a given product's rewrite has been applied.

Output: llms.txt on stdout, stats on stderr.
"""
import gzip, html, json, os, re, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, "cat")
PLAN = os.path.join(HERE, "..", "bulk", "rewrite", "plan.json.gz")
SHOP = "https://drinkshouse247.co.uk"

# Products that are not merchandise and must never appear in the catalog.
EXCLUDE_HANDLES = {"service-fee_1hjfl1av22lo"}

LD = re.compile(r'<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>.*?</script>', re.I | re.S)
SCRIPT = re.compile(r'<script[^>]*>.*?</script>', re.I | re.S)
STYLE = re.compile(r'<style[^>]*>.*?</style>', re.I | re.S)
TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')

# The two description layouts in use both mark their opening summary paragraphs
# with a class, so prefer those over a flat tag-strip -- otherwise badge and
# spec-table text gets concatenated into the summary as meaningless run-on.
LEDE = re.compile(
    r'<p[^>]*class\s*=\s*["\'][^"\']*(?:lux-lede|lux-story|dh-lede|dh-story)[^"\']*["\'][^>]*>(.*?)</p>',
    re.I | re.S)


def prose(html_text, limit=320):
    """Visible prose only: no CSS, no JSON-LD, no markup, collapsed whitespace."""
    if not html_text:
        return ""
    lede = LEDE.findall(html_text)
    if lede:
        t = " ".join(lede)
        t = TAG.sub(" ", t)
        t = html.unescape(t)
        t = WS.sub(" ", t).strip()
        if t:
            if len(t) <= limit:
                return t
            return t[:limit].rsplit(" ", 1)[0] + "\u2026"
    t = LD.sub(" ", html_text)
    t = STYLE.sub(" ", t)
    t = SCRIPT.sub(" ", t)
    t = TAG.sub(" ", t)
    t = html.unescape(t)
    t = WS.sub(" ", t).strip()
    if len(t) <= limit:
        return t
    cut = t[:limit].rsplit(" ", 1)[0]
    return cut + "…"


def money(a):
    f = float(a)
    return f"£{f:,.2f}".rstrip("0").rstrip(".") if f % 1 else f"£{int(f):,}"


def main():
    products = json.load(open(os.path.join(CAT, "products.json")))
    tax = json.load(open(os.path.join(CAT, "tax_all.json")))
    plan = json.load(gzip.open(PLAN, "rt", encoding="utf-8"))

    live = [
        p for p in products.values()
        if p.get("onlineStoreUrl") and p["handle"] not in EXCLUDE_HANDLES
    ]
    live.sort(key=lambda p: ((p.get("productType") or "~").lower(), p["title"].lower()))

    colls = [c for c in tax["collections"] if c["productsCount"]["count"] > 0]
    colls.sort(key=lambda c: -c["productsCount"]["count"])
    pages = sorted(tax["pages"], key=lambda p: p["title"].lower())
    blogs = tax["blogs"]
    articles = [(b["handle"], a) for b in blogs for a in b["articles"]["nodes"]]

    out = []
    w = out.append

    w("# Drinks House 247 — Full Store Catalog")
    w(f"> Store: [drinkshouse247.co.uk]({SHOP})")
    w("> 24-hour licensed alcohol delivery across London and the UK. Instant delivery")
    w("> in Greater London in 30–45 minutes, same-day up to 6 hours, and next-day")
    w("> nationwide on orders placed before 2pm.")
    w(f"> Last updated: {date.today().isoformat()}")
    w(f"> Products: {len(live)} | Collections: {len(colls)} | Pages: {len(pages)} | "
      f"Blogs: {len(blogs)} | Articles: {len(articles)}")
    w("")
    w("This file lists the complete published catalog. Prices are in GBP and were")
    w("correct at the timestamp above; the product page is authoritative.")
    w("")
    w("---")
    w("")
    w("## Products")
    w("")

    by_type = {}
    for p in live:
        by_type.setdefault((p.get("productType") or "Other").strip() or "Other", []).append(p)

    for ptype in sorted(by_type, key=lambda k: (-len(by_type[k]), k.lower())):
        items = by_type[ptype]
        w(f"### {ptype.title()} ({len(items)})")
        w("")
        for p in items:
            pid = p["id"]
            desc_src = plan[pid]["new"] if pid in plan else p.get("descriptionHtml", "")
            d = prose(desc_src)
            lo = p["priceRangeV2"]["minVariantPrice"]["amount"]
            hi = p["priceRangeV2"]["maxVariantPrice"]["amount"]
            price = money(lo) if lo == hi else f"{money(lo)}–{money(hi)}"
            variants = p["variants"]["nodes"]
            instock = any(v["availableForSale"] for v in variants)

            w(f"#### [{p['title']}]({p['onlineStoreUrl']})")
            w(f"- Category: {ptype}")
            if p.get("vendor"):
                w(f"- Brand: {p['vendor']}")
            w(f"- Price: {price} GBP")
            w(f"- Availability: {'In stock' if instock else 'Out of stock'}")
            if d:
                w(f"- Description: {d}")
            if len(variants) > 1:
                w("- Options:")
                for v in variants:
                    mark = "in stock" if v["availableForSale"] else "out of stock"
                    sku = f" · SKU {v['sku']}" if v.get("sku") else ""
                    w(f"  - {v['title']} — {money(v['price'])}{sku} ({mark})")
            elif variants and variants[0].get("sku"):
                w(f"- SKU: {variants[0]['sku']}")
            w("")

    w("---")
    w("")
    w("## Collections")
    w("")
    for c in colls:
        w(f"- [{c['title']}]({SHOP}/collections/{c['handle']}) — {c['productsCount']['count']} products")
    w("")

    w("---")
    w("")
    w("## Guides & Information Pages")
    w("")
    for pg in pages:
        w(f"- [{pg['title']}]({SHOP}/pages/{pg['handle']})")
    w("")

    if articles:
        w("---")
        w("")
        w("## Articles")
        w("")
        for bh, a in articles:
            w(f"- [{a['title']}]({SHOP}/blogs/{bh}/{a['handle']})")
        w("")

    text = "\n".join(out)
    sys.stdout.write(text)
    sys.stderr.write(
        f"[llms.txt] {len(live)} products, {len(colls)} collections, {len(pages)} pages, "
        f"{len(articles)} articles | {len(text.encode('utf-8')):,} bytes\n"
    )


if __name__ == "__main__":
    main()
