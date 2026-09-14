"""Normalise internal links in Shopify article/page bodies.

Three fixes, all deterministic and content-preserving:
  1. Absolute internal URLs -> relative, so locale subfolders (/ar, /ru, /zh) are
     preserved when a reader follows a link. An absolute URL ejects a localised
     reader back to the English site.
  2. Bare-domain links -> "/".
  3. target="_blank" and its companion rel="noopener noreferrer" stripped from
     INTERNAL links only. External links keep both.

Usage:  python3 fix_links.py <json-file> <key>   # prints JSON-escaped fixed body
"""
import json, re, sys

DOMAIN = r'https?://(?:www\.)?drinkshouse247\.co\.uk'
ANCHOR = re.compile(r'<a\s+[^>]*>', re.I)


def fix(body: str) -> tuple[str, dict]:
    stats = {"abs_to_rel": 0, "blank_stripped": 0}

    def fix_anchor(m: re.Match) -> str:
        tag = m.group(0)
        href = re.search(r'href="([^"]*)"', tag, re.I)
        if not href:
            return tag
        url = href.group(1)
        internal = bool(re.match(DOMAIN + r'(/|$)', url)) or url.startswith('/')
        if not internal:
            return tag
        new_url = re.sub(DOMAIN, '', url) or '/'
        if new_url != url:
            stats["abs_to_rel"] += 1
            tag = tag.replace(f'href="{url}"', f'href="{new_url}"')
        if re.search(r'target="_blank"', tag, re.I):
            stats["blank_stripped"] += 1
            tag = re.sub(r'\s*target="_blank"', '', tag, flags=re.I)
            tag = re.sub(r'\s*rel="noopener noreferrer"', '', tag, flags=re.I)
            tag = re.sub(r'\s*rel="noopener"', '', tag, flags=re.I)
        return re.sub(r'\s+>', '>', tag)

    out = ANCHOR.sub(fix_anchor, body)
    leftover = re.findall(DOMAIN, out)
    if leftover:
        raise SystemExit(f"FAILED: {len(leftover)} domain refs remain (non-anchor context)")
    return out, stats


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))["data"][sys.argv[2]]
    fixed, stats = fix(data["body"])
    sys.stderr.write(f"{data['handle']}: {stats}  {len(data['body'])} -> {len(fixed)} chars\n")
    print(json.dumps(fixed, ensure_ascii=False))
