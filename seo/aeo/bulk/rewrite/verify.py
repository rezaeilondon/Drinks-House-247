#!/usr/bin/env python3
"""Re-prove the transformation is lossless for every product still to be done.

For each rewrite it checks that the visible prose (all tags, <style> and
<script type="application/ld+json"> stripped) is byte-identical before and
after, and that every <style> block survives verbatim. Exits non-zero if any
product fails, so it can gate a run.
"""
import gzip, json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
plan = json.load(gzip.open(os.path.join(D, "plan.json.gz"), "rt", encoding="utf-8"))

LD = re.compile(r'<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>.*?</script>\s*', re.I | re.S)
ST = re.compile(r'<style[^>]*>.*?</style>\s*', re.I | re.S)
TAG = re.compile(r'<[^>]+>')

def prose(h):
    return re.sub(r'\s+', ' ', TAG.sub(' ', ST.sub('', LD.sub('', h)))).strip()

fails = 0
for pid, v in plan.items():
    if prose(v["old"]) != prose(v["new"]):
        print(f"PROSE MISMATCH {pid} {v['handle']}")
        fails += 1
    if sorted(s.strip() for s in ST.findall(v["old"])) != sorted(s.strip() for s in ST.findall(v["new"])):
        print(f"STYLE LOST {pid} {v['handle']}")
        fails += 1

print(f"checked {len(plan)} products | failures: {fails}")
sys.exit(1 if fails else 0)
