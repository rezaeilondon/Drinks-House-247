"""Normalise internal links and canonical hosts in Shopify article/page bodies.

Four deterministic, content-preserving fixes:
  1. Absolute internal URLs in href -> relative, so locale subfolders (/ar, /ru,
     /zh) survive a click. An absolute URL ejects a localised reader to English.
  2. Bare-domain hrefs -> "/".
  3. target="_blank" / target="_new" (and the companion rel) stripped from
     INTERNAL links only. External links keep both. Both variants occur in this
     store's content - _new was missed on the first pass.
  4. Any remaining www host -> apex. These are JSON-LD values (author.url,
     publisher.url, mainEntityOfPage.@id) which must stay ABSOLUTE, so they are
     rewritten to the canonical apex rather than made relative.

Canonical host confirmed by the owner: https://drinkshouse247.co.uk (no www) --
the Google Search Console property and Shopify primary domain.
"""
import json, re, sys

DOMAIN = r'https?://(?:www\.)?drinkshouse247\.co\.uk'
APEX = 'https://drinkshouse247.co.uk'
ANCHOR = re.compile(r'<a\s+[^>]*>', re.I)


def fix(body: str) -> tuple[str, dict]:
    stats = {"abs_to_rel": 0, "blank_stripped": 0, "host_canonicalised": 0}

    def fix_anchor(m):
        tag = m.group(0)
        href = re.search(r'href="([^"]*)"', tag, re.I)
        if not href:
            return tag
        url = href.group(1)
        if not (re.match(DOMAIN + r'(/|$)', url) or url.startswith('/')):
            return tag                      # external: leave entirely alone
        new = re.sub(DOMAIN, '', url) or '/'
        if new != url:
            stats["abs_to_rel"] += 1
            tag = tag.replace(f'href="{url}"', f'href="{new}"')
        if re.search(r'target="(?:_blank|_new)"', tag, re.I):
            stats["blank_stripped"] += 1
            tag = re.sub(r'\s*target="(?:_blank|_new)"', '', tag, flags=re.I)
            tag = re.sub(r'\s*rel="noopener noreferrer"', '', tag, flags=re.I)
            tag = re.sub(r'\s*rel="noopener"', '', tag, flags=re.I)
        return re.sub(r'\s+>', '>', tag)

    out = ANCHOR.sub(fix_anchor, body)
    stats["host_canonicalised"] = len(re.findall(r'https?://www\.drinkshouse247\.co\.uk', out))
    out = re.sub(r'https?://www\.drinkshouse247\.co\.uk', APEX, out)
    assert 'www.drinkshouse247' not in out
    return out, stats
