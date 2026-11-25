#!/usr/bin/env python3
"""Move every stated age-verification policy from Challenge 21 to Challenge 25.

Run against a fresh snapshot of pages/articles/products. Deterministic: the same
input always produces the same output, and every substitution is reported.

The dangerous failure mode is a blanket 21 -> 25, which would rewrite whisky age
statements ("Glenfiddich 21 Year Old", "aged 21 years"). So the only "21"s touched
are the ones matched by the explicit patterns below, and the legal purchase age
("18 or over", "18+", "over 18") is never touched at all.
"""
import re

OLD_HANDLE = '/pages/challenge-21'
NEW_HANDLE = '/pages/challenge-25'

# (name, pattern, replacement). Order matters: longest/most specific first.
RULES = [
    ("handle",        re.compile(re.escape(OLD_HANDLE)),                      NEW_HANDLE),
    ("challenge-N",   re.compile(r'Challenge(\s|&nbsp;|-)*21\b'),             r'Challenge\g<1>25'),
    ("age-of-21",     re.compile(r'\b(under|below)(\s+the\s+age\s+of\s+)21\b', re.I), r'\1\g<2>25'),
    ("under-21",      re.compile(r'\b(under|below)(\s+)21\b', re.I),          r'\1\g<2>25'),
    ("appear-21",     re.compile(r'\b(appears?|appear|looks?|look)(\s+)21\b', re.I), r'\1\g<2>25'),
]

# Things that must survive untouched. Checked before and after; counts must match.
GUARDS = [
    re.compile(r'\b18\s*\+|\b18\s+or\s+over|\bover\s+18\b|\b18\s+years', re.I),
    re.compile(r'\b\d{1,2}\s*[- ]?year[- ]?old\b', re.I),   # whisky/rum age statements
    re.compile(r'\baged\s+\d{1,2}\b', re.I),
]


def transform(html):
    """Return (new_html, [(rule_name, matched_text, context), ...])."""
    before = [len(g.findall(html)) for g in GUARDS]
    hits = []
    out = html
    for name, pat, rep in RULES:
        def _sub(m):
            s, e = m.span()
            hits.append((name, m.group(0), out[max(0, s - 55):e + 55].replace('\n', ' ')))
            return m.expand(rep) if '\\' in rep or '\\g' in rep else rep
        out = pat.sub(_sub, out)

    after = [len(g.findall(out)) for g in GUARDS]
    if before != after:
        raise AssertionError(f'guard tripped: protected text changed {before} -> {after}')
    # Nothing may still claim Challenge 21.
    assert not re.search(r'Challenge(\s|&nbsp;|-)*21\b', out), 'Challenge 21 survived'
    assert OLD_HANDLE not in out, 'old handle survived'
    return out, hits
