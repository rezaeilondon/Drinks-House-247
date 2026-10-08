"""Build the next batch of product-description schema fixes.

Smart SEO already outputs a live Product JSON-LD on every product page, so the
hand-written Product block embedded in some descriptions is a duplicate with a
hard-coded price and stock status. This script removes that block (and fixes
any leftover "Challenge 21" wording) for the next N products that still have it.

Input: a Shopify bulk-export JSONL of products {id, handle, status, descriptionHtml}.
Output: OUT/NNN.txt files - line 1 is the productUpdate mutation, line 2 the
variables JSON (ASCII-escaped) - plus OUT/batch.tsv listing what was queued.

Usage: python3 -I schema_batch.py live.jsonl OUT_DIR [COUNT]
"""
import json
import os
import re
import sys

BLOCK = re.compile(r'\n*<script type="application/ld\+json">.*?</script>\n?', re.S)
ORDER = {"ACTIVE": 0, "DRAFT": 1, "ARCHIVED": 2}
MUTATION = ('mutation($b0: String!) { b0: productUpdate(product: {id: "%s", '
            'descriptionHtml: $b0}) { product { id } userErrors { field message } } }')


def main(src, out, count=29):
    rows = [json.loads(line) for line in open(src)]
    todo = sorted(
        (r for r in rows if "application/ld+json" in (r.get("descriptionHtml") or "")),
        key=lambda r: (ORDER.get(r["status"], 3), r["handle"]),
    )
    os.makedirs(out, exist_ok=True)
    index = []
    for i, r in enumerate(todo[:count], 1):
        html = r["descriptionHtml"]
        new = BLOCK.sub("\n", html, count=1).replace("Challenge 21", "Challenge 25")
        assert "ld+json" not in new and len(html) - len(new) < 3000, r["handle"]
        with open(os.path.join(out, "%03d.txt" % i), "w") as f:
            f.write(MUTATION % r["id"] + "\n" + json.dumps({"b0": new}, ensure_ascii=True) + "\n")
        index.append("%03d\t%s\t%s" % (i, r["status"], r["handle"]))
    with open(os.path.join(out, "batch.tsv"), "w") as f:
        f.write("\n".join(index) + "\n")
    print("remaining with embedded schema: %d; queued this batch: %d" % (len(todo), len(index)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 29)
