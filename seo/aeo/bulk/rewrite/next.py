#!/usr/bin/env python3
"""Emit the next batch of productUpdate mutations as a single GraphQL document.

Reads state from this directory (repo-relative, so any session can resume):
  plan.json.gz  {product_gid: {handle, title, old, new}}  -- all 1,248 rewrites
  order.json    priority order of product gids
  done.json     gids already applied

Writes pending.json (the gids in the emitted batch). Nothing is marked done
here -- run commit.py only AFTER the mutation returns with empty userErrors.

Usage: python3 next.py [byte_budget]      (default 11000)
"""
import gzip, json, os, sys
import fixes

D = os.path.dirname(os.path.abspath(__file__))
plan = json.load(gzip.open(os.path.join(D, "plan.json.gz"), "rt", encoding="utf-8"))
order = json.load(open(os.path.join(D, "order.json")))
SF = os.path.join(D, "done.json")
done = set(json.load(open(SF))) if os.path.exists(SF) else set()

BUDGET = int(sys.argv[1]) if len(sys.argv) > 1 else 11000
# fixups.json: products already rewritten that must be re-sent because a fix in
# fixes.py changed them. They go first.
FF = os.path.join(D, "fixups.json")
fixups = json.load(open(FF)) if os.path.exists(FF) else []
rem = fixups + [p for p in order if p not in done]
if not rem:
    sys.stderr.write("ALL DONE\n")
    sys.exit(0)

batch, tot = [], 0
for p in rem:
    n = len(fixes.apply(p, plan[p]["new"])) + len(p) + 140
    if batch and tot + n > BUDGET:
        break
    batch.append(p)
    tot += n

out = ["mutation {"]
for i, pid in enumerate(batch):
    v = plan[pid]
    out.append(
        f'  p{i}: productUpdate(product: {{id: "{pid}", '
        f'descriptionHtml: {json.dumps(fixes.apply(pid, v["new"]), ensure_ascii=True)}}}) '
        f'{{ product {{ id }} userErrors {{ field message }} }}'
    )
out.append("}")
m = "\n".join(out)

# The harness persists rather than displays any tool result over ~30 KB, and a
# document we cannot see is one we cannot transcribe. Drop trailing products
# until the emitted mutation is comfortably under that ceiling.
CEILING = 29000
while len(m) > CEILING and len(batch) > 1:
    batch.pop()
    out = ["mutation {"]
    for i, pid in enumerate(batch):
        v = plan[pid]
        out.append(
            f'  p{i}: productUpdate(product: {{id: "{pid}", '
            f'descriptionHtml: {json.dumps(fixes.apply(pid, v["new"]), ensure_ascii=True)}}}) '
            f'{{ product {{ id }} userErrors {{ field message }} }}'
        )
    out.append("}")
    m = "\n".join(out)

json.dump(batch, open(os.path.join(D, "pending.json"), "w"))
sys.stderr.write(
    f"[BATCH] {len(batch)} products, {len(m):,} chars | done {len(done)}/{len(order)} "
    f"| fixups queued {len(fixups)} | remaining after this: {len(rem) - len(batch)}\n"
)
print(m)
