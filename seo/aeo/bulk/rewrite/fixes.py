"""Content fixes layered on top of plan.json.gz at emission time.

plan.json.gz is left untouched so verify.py keeps proving the rewrite itself
is lossless. Anything that deliberately changes what a shopper sees lives
here instead, and next.py applies it to every description it emits.

  copy-fixes.json   exact string replacements for one product
  ICON_RULES        serving-card emoji that don't match their label
"""
import json, os, re

D = os.path.dirname(os.path.abspath(__file__))
_copy = json.load(open(os.path.join(D, "copy-fixes.json")))

# (wrong icon, label test, right icon). The label test keeps each swap to the
# cards where the icon is actually wrong -- sushi is fine on a sushi card.
ICON_RULES = [
    ("\U0001F989", lambda l: "Meat" in l, "\U0001F356"),                  # owl -> meat
    ("\U0001F95B", lambda l: l.startswith("Neat") or l == "On the Rocks",
     "\U0001F943"),                                                         # milk -> tumbler
    ("\U0001F95B", lambda l: "Tonic" in l or "Soda" in l, "\U0001F964"),  # milk -> long drink
    ("\U0001F363", lambda l: "Chocolate" in l, "\U0001F36B"),             # sushi -> chocolate
]
_CARD = re.compile(r'(<span class="dh-ico">)(.*?)(</span><div class="dh-label">)(.*?)(</div>)')


def _swap(m):
    ico, label = m.group(2), m.group(4)
    for bad, test, good in ICON_RULES:
        if ico == bad and test(label):
            ico = good
            break
    return m.group(1) + ico + m.group(3) + label + m.group(5)


def apply_copy(pid, html):
    for f in _copy:
        if f["product"] == pid:
            html = html.replace(f["old"], f["new"])
    return html


def apply(pid, html):
    return _CARD.sub(_swap, apply_copy(pid, html))
