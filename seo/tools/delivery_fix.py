#!/usr/bin/env python3
"""Normalise old delivery wording in product descriptions.

Current offer: 30-45 minutes in London (24/7), next-day UK-wide, and same
day for business addresses that order by 4pm. Old copy promised a 6-hour
same-day service, a 2pm next-day cut-off and a 1-2 day option.

Usage: python3 -I delivery_fix.py <export.jsonl> <outdir>
Writes <outdir>/fixed.jsonl ({id, handle, descriptionHtml}), a Shopify
product CSV (Handle, Body (HTML)) and residual.tsv listing products that
still contain old wording after the automatic rules.
"""
import csv
import json
import os
import re
import sys

OLD = re.compile(r'(?<!keeps cold )up to [36] h(?:ou)?rs|before 2pm|1[–-]2 (?:business )?days?\b'
                 r'|within six hours|Challenge 21|application/ld\+json', re.I)

# Same transforms as schema_batch.py, so one import also finishes the schema cleanup.
LDJSON = re.compile(r'\n*<script type="application/ld\+json">.*?</script>\n?', re.S)

ONE_LINER = re.compile(
    r'<b>Instant delivery</b> across Greater London in 30–45 mins · '
    r'<b>Same-day</b> up to [36] hrs · '
    r'<b>Next-day</b> nationwide on orders before 2pm\.')
ONE_LINER_NEW = ('<b>London</b> 30–45 minutes, 24/7 · '
                 '<b>Next-day</b> delivery UK-wide · '
                 '<b>Same-day</b> for business addresses ordering by 4pm.')

LUX_BLOCK_OLD = (
    '<p><b>Instant Delivery</b> — Greater London, 30–45 minutes</p>\n'
    '<p><b>Same Day Delivery</b> — Greater London, up to 6 hours</p>\n'
    '<p><b>Next Day Delivery</b> — Mainland UK, order before 2pm</p>\n'
    '<p><b>1–2 Day Delivery</b> — Mainland UK</p>\n'
    '<p><b>Gift Packaging</b> — available on same day, next day and 1–2 day services</p>')
LUX_BLOCK_NEW = (
    '<p><b>London Delivery</b> — Greater London, 30–45 minutes, 24/7</p>\n'
    '<p><b>Next-Day Delivery</b> — UK-wide</p>\n'
    '<p><b>Same-Day Business Delivery</b> — business addresses ordering by 4pm</p>\n'
    '<p><b>Gift Packaging</b> — added at checkout</p>')

TABLE = re.compile(r'<table[^>]*>(?:(?!</table>).)*?Delivery and Gift Options.*?</table>', re.S)
TABLE_NEW = (
    '<table>\n<thead>\n<tr>\n<th>Delivery and Gift Options</th>\n<th>Coverage Area</th>\n'
    '<th>Estimated Delivery Time</th>\n</tr>\n</thead>\n<tbody>\n'
    '<tr>\n<td>London Delivery</td>\n<td>Greater London</td>\n<td>30–45 mins, 24/7</td>\n</tr>\n'
    '<tr>\n<td>Next-Day Delivery</td>\n<td>UK-wide</td>\n<td>Next day</td>\n</tr>\n'
    '<tr>\n<td>Same-Day Business Delivery</td>\n<td>Business addresses (order by 4pm)</td>\n'
    '<td>Same day</td>\n</tr>\n'
    '<tr>\n<td>Gift Packaging</td>\n<td>All delivery options</td>\n<td>Added at checkout</td>\n</tr>\n'
    '</tbody>\n</table>')

SENTENCES = [
    ('30 to 45 minutes across Greater London, or same day within six hours. '
     'Order before 2pm for next-day delivery to mainland UK.',
     '30 to 45 minutes across Greater London, any hour. Next-day delivery UK-wide, '
     'and same day for business addresses that order by 4pm.'),
    ('Available at checkout on same-day, next-day and 1–2 day services.',
     'Available at checkout on every delivery option.'),
    ('Gift packaging can also be added at checkout on same-day, next-day and 1–2 day services.',
     'Gift packaging can also be added at checkout on every delivery option.'),
    ('Same-day delivery is available across Greater London within six hours, and next-day '
     'to mainland UK if you order before 2pm.',
     'We deliver across Greater London in 30–45 minutes, any hour, and next-day UK-wide; '
     'business addresses that order by 4pm can have it the same day.'),
    ('Express in 1–2 business days, standard in 3–5. Rates shown at checkout.',
     'Next-day delivery across the UK mainland. Rates shown at checkout.'),
    ('Express UK in 1–2 business days.', 'Next-day delivery UK-wide.'),
    ('UK express 1–2 business days', 'UK next-day delivery'),
]


def fix(d):
    before = len(d)
    d = LDJSON.sub('\n', d, count=1)
    assert before - len(d) < 3000
    d = d.replace('Challenge 21', 'Challenge 25')
    d = ONE_LINER.sub(ONE_LINER_NEW, d)
    d = d.replace(LUX_BLOCK_OLD, LUX_BLOCK_NEW)
    d = TABLE.sub(lambda m: TABLE_NEW if OLD.search(m.group(0)) else m.group(0), d)
    for old, new in SENTENCES:
        d = d.replace(old, new)
    return d


def main(src, out):
    os.makedirs(out, exist_ok=True)
    changed = residual = 0
    with open(os.path.join(out, 'fixed.jsonl'), 'w') as fj, \
         open(os.path.join(out, 'products.csv'), 'w', newline='') as fc, \
         open(os.path.join(out, 'residual.tsv'), 'w') as fr:
        w = csv.writer(fc)
        w.writerow(['Handle', 'Body (HTML)'])
        for line in open(src):
            o = json.loads(line)
            d = o.get('descriptionHtml') or ''
            if not OLD.search(d):
                continue
            new = fix(d)
            if new != d:
                changed += 1
                fj.write(json.dumps({'id': o['id'], 'handle': o['handle'],
                                     'descriptionHtml': new}) + '\n')
                w.writerow([o['handle'], new])
            for m in OLD.finditer(new):
                residual += 1
                ctx = re.sub(r'\s+', ' ', new[max(0, m.start() - 120):m.end() + 60])
                fr.write(f"{o['handle']}\t{ctx}\n")
    print(f'changed {changed}; residual matches {residual}')


if __name__ == '__main__':
    main(*sys.argv[1:3])
