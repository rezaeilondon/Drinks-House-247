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
    ("\U0001F9BF", lambda l: True, "\U0001F41F"),                        # mechanical leg -> fish
    ("\U0001FB4F", lambda l: True, "\U0001F9AA"),                        # legacy block glyph -> oyster
    ("\U0001FB7F", lambda l: True, "\U0001F99E"),                        # legacy block glyph -> lobster
    ("\U0001FB79", lambda l: True, "\U0001F980"),                        # legacy block glyph -> crab
    ("\U0001F9F2", lambda l: "Charcuterie" in l, "\U0001F953"),         # magnet -> cured meat
    ("\U0001F9F2", lambda l: "Antipast" in l, "\U0001FAD2"),            # magnet -> olive
    ("\U0001F96A", lambda l: "Lamb" in l, "\U0001F356"),                # sandwich -> roast meat
    ("\U0001F971", lambda l: "Pie" in l, "\U0001F967"),                 # yawning face -> pie
    ("\U0001F999", lambda l: "Tempura" in l, "\U0001F364"),             # llama -> tempura prawn
    ("\U0001F34C", lambda l: "Nut" in l, "\U0001F95C"),                 # banana -> nuts
    ("\U0001F36A", lambda l: "Chocolate" in l, "\U0001F36B"),           # cookie -> chocolate
    ("\U0001F7EB", lambda l: "Rose" in l, "\U0001F339"),                # brown square -> rose
    ("\U0001F345", lambda l: "Tart" in l, "\U0001F967"),                # tomato -> tart
    ("\U0001F345", lambda l: "Fig" in l, "\U0001F347"),                 # tomato -> dried fruit
    ("\U0001F345", lambda l: l == "Fresh Fruit", "\U0001F353"),         # tomato -> fruit
    ("\U0001F357", lambda l: "Steak" in l, "\U0001F969"),               # drumstick -> steak
    ("\U0001F357", lambda l: "Ribs" in l, "\U0001F356"),                # drumstick -> ribs
    ("\U0001F377", lambda l: "Whisky" in l, "\U0001F943"),              # wine glass -> tumbler
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
