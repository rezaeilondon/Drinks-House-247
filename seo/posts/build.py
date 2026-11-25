"""Build scheduled blog articles (body HTML + JSON-LD + articleCreate variables).

Each article module in this folder defines ARTICLE = {...}. This script renders the
body, generates FAQPage JSON-LD from the same FAQ list used for the visible text (so
they can never drift apart), validates the JSON, checks length/limits, and writes
<slug>.vars.json ready for articleCreate.

    python3 build.py            # build all
    python3 build.py <slug>     # build one, print its variables
"""
import html, importlib.util, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
BLOG_ID = "gid://shopify/Blog/27034058814"
BANNED = ["unlock", "elevate", "dive into", "fast-paced world", "!"]


def faq_html(faqs):
    out = ["<h2>Frequently asked questions</h2>"]
    for q, a in faqs:
        out.append(f"<h3>{html.escape(q, quote=False)}</h3>\n<p>{html.escape(a, quote=False)}</p>")
    return "\n".join(out)


def jsonld(a):
    graph = [
        {
            "@type": "Article",
            "headline": a["title"],
            "description": a["description_tag"],
            "datePublished": a["date"],
            "author": {"@type": "Organization", "name": "Drinks House 247"},
            "publisher": {"@type": "Organization", "name": "Drinks House 247",
                          "url": "https://drinkshouse247.co.uk"},
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": ans}}
                for q, ans in a["faqs"]
            ],
        },
    ]
    if a.get("local_business"):
        graph.append({
            "@type": "LocalBusiness",
            "name": "Drinks House 247",
            "url": "https://drinkshouse247.co.uk",
            "telephone": "+44 20 3488 3266",
            "areaServed": "London",
            "openingHours": "Mo-Su 00:00-23:59",
        })
    doc = {"@context": "https://schema.org", "@graph": graph}
    s = json.dumps(doc, ensure_ascii=False, separators=(",", ":"))
    json.loads(s)  # must parse
    return s


def render(a):
    body = (
        f"<h1>{html.escape(a['title'], quote=False)}</h1>\n\n"
        f"<p><strong>{a['answer']}</strong></p>\n\n"
        f"{a['body'].strip()}\n\n"
        f"{faq_html(a['faqs'])}\n\n"
        f"{a['closing'].strip()}\n\n"
        f"<script type=\"application/ld+json\">\n{jsonld(a)}\n</script>"
    )
    return body


def check(a, body):
    problems = []
    text = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    words = len(text.split())
    ans_words = len(re.sub(r"<[^>]+>", "", a["answer"]).split())
    if not 40 <= ans_words <= 60:
        problems.append(f"direct answer {ans_words} words (want 40-60)")
    if "Drinks House 247" not in a["answer"]:
        problems.append("direct answer does not name Drinks House 247")
    if not 900 <= words <= 1400:
        problems.append(f"{words} words (want 900-1400)")
    if len(a["title_tag"]) > 60:
        problems.append(f"title_tag {len(a['title_tag'])} chars")
    if len(a["description_tag"]) > 155:
        problems.append(f"description_tag {len(a['description_tag'])} chars")
    if not 140 <= len(a["summary"]) <= 160:
        problems.append(f"summary {len(a['summary'])} chars (want 140-160)")
    if len(a["handle"]) > 70:
        problems.append("handle too long")
    if "<table" not in body:
        problems.append("no table")
    low = text.lower()
    for b in BANNED:
        if b in low:
            problems.append(f"banned phrase {b!r}")
    if "www." in body:
        problems.append("www. in body")
    return words, problems


def variables(a, body):
    art = {
        "blogId": BLOG_ID,
        "title": a["title"],
        "handle": a["handle"],
        "body": body,
        "summary": a["summary"],
        "author": {"name": "Drinks House 247"},
        "tags": a["tags"],
        "isPublished": True,
        "metafields": [
            {"namespace": "global", "key": "title_tag", "type": "single_line_text_field",
             "value": a["title_tag"]},
            {"namespace": "global", "key": "description_tag", "type": "single_line_text_field",
             "value": a["description_tag"]},
        ],
    }
    if a.get("publish_at"):
        # Shopify rejects isPublished=true alongside a future publishDate; a
        # scheduled article is created unpublished and goes live on its date.
        art["isPublished"] = False
        art["publishDate"] = a["publish_at"]
    return {"article": art}


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.ARTICLE


def links(body):
    return sorted(set(re.findall(r'href="(/[^"]+)"', body)))


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    ok = True
    for p in sorted(HERE.glob("a*_*.py")):
        a = load(p)
        if only and a["handle"] != only:
            continue
        body = render(a)
        words, problems = check(a, body)
        v = variables(a, body)
        (HERE / f"{a['handle']}.vars.json").write_text(json.dumps(v, ensure_ascii=False, indent=1))
        status = "OK" if not problems else "FIX: " + "; ".join(problems)
        print(f"{a['date']}  {a['handle']:<48} {words:>5}w  {status}")
        print("    links:", " ".join(links(body)))
        ok &= not problems
        if only:
            print(json.dumps(v, ensure_ascii=False))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
