# Fixing `brand` and `gtin` for the Microsoft Copilot feed

Two fields block product matching. They need completely different treatment, and the
difference matters.

---

## 1. Brand — fixed by derivation (in progress)

`vendor` maps to `brand` in every feed, and it read "Drinks House 247" on the great
majority of the catalogue, so listings described the shop rather than the distillery.

**Correcting a figure stated earlier in this session:** the "1,253 of 1,257" claim
conflated two denominators. 1,253 of **1,449 total** products carried the retailer as
vendor. Among the **1,257 active** products the figure was **1,076**. Still the
overwhelming majority, but the earlier sentence was wrong.

`brand_from_title.py` derives the producer from the product title. It is deliberately
**high precision, not high coverage** — a wrong brand is worse than none, because it
mismatches the product against another company's catalogue entry.

Two matchers:

- **Curated** (661 products): an explicit producer list, longest-name-first so
  "Johnnie Walker Blue Label" cannot be shadowed by a shorter entry, word-boundary
  anchored so "Au" cannot match inside "Australia".
- **Estate** (64 products): French and Italian estate naming, where the estate *is* the
  brand — `Château Larose Trintaudon`. Start-of-title only, stops at the first varietal
  or appellation word, so "Château Haut-Blanville **Merlot** 75cl" stops before Merlot.

Appellations and varietals are explicitly excluded. "Bourgogne Chardonnay" and
"Puligny-Montrachet" are places, not producers.

A `CANON` table forces one spelling per producer, because feeds match exact strings:
`Moet`, `Moët` and `Moet & Chandon` all resolve to **Moët & Chandon**.

**Result: 721 products written, across 209 distinct brands.** All 721 are listed in
`products-brand-vendor.csv`. The remaining products are left untouched and listed in
`products-brand-unmatched.csv` — mostly generic lines ("Orange Juice", "Mixed Red",
"Service Fee") and wines whose producer is not in the curated list.

Store-wide state after the run, read back from the Admin API rather than inferred
from the write responses:

| | Products |
|---|---|
| Total in catalogue | 1,449 |
| Carrying a real brand | 827 (279 distinct) |
| — written by this run | 721 |
| — already branded beforehand | 106 |
| Still `Drinks House 247` | 622 (444 of them active) |

### Three bugs found and fixed while building it

1. A curly apostrophe in "Chateau d’Esclans" did not match the straight one in the list,
   silently costing a producer match. `_fold()` now normalises quotes and dashes.
2. "Les" was in the stop-list, so "Château **Les** Maurins" was rejected. Articles may
   now appear inside an estate name but cannot start one.
3. The estate matcher took three words and produced
   "Château Larose Trintaudon **Haut-Médoc**" — an appellation. Corrected by hand.

### Delivery status

Applied through the Admin API in batches. Shopify **times out partway through large
batched mutations while still applying the earlier ones**, returning a generic
`upstream_error`, so progress was verified by re-querying rather than trusting the
response. Batch size reduced to 40. Re-applying a vendor already set is a no-op, so
overlapping batches are safe.

`products-brand-vendor.csv` holds the full mapping and can complete the job by import.

---

## 2. GTIN — NOT fixed, and deliberately not

**No barcodes were invented, and none should be.**

A GTIN is a fact printed on the bottle, not a value that can be derived from a title.
Generating plausible-looking EANs would be worse than leaving the field empty:

- A wrong GTIN matches your product to **somebody else's product** in Microsoft's and
  Google's catalogues. The listing would then inherit the wrong images, reviews and
  price comparisons.
- Feeds validate GTIN check digits. A fabricated number either fails validation, or —
  worse — passes and points somewhere real.
- Supplying knowingly incorrect identifiers breaches the feed terms of every major
  shopping platform.

There is no shortcut here. The barcodes have to come from a source that actually knows
them:

1. **Your wholesalers.** Costco, DWG and Amathus can all supply an EAN against each
   product line — usually as a spreadsheet column that already exists in their catalogue
   export. This is the fastest route by a distance and covers most of the range in one
   request.
2. **Scan the stock.** A phone barcode app and a spreadsheet will clear a shelf quickly,
   and it is the only route for lines no supplier will export.
3. **A GTIN lookup service**, checked against the physical bottle before use.

`products-gtin-TEMPLATE.csv` lists every active product with an empty barcode column,
ready to fill from any of those sources. Hand it back filled and the values can be
written to `variant.barcode` in bulk.

### One thing worth checking first

If Microsoft is rejecting these products on **alcohol policy** rather than feed quality,
GTINs will not change the outcome. The Copilot channel's own rejection list will say
which. That check costs minutes; sourcing 1,257 barcodes does not.

### Verification, and what a read-back caught

The writes went out in batches of 60 aliased `productUpdate` mutations. Shopify times
out partway through larger batches while still applying the earlier mutations and
returning a generic `upstream_error`, so batch size is a correctness constraint, not a
performance one. Every batch returned `userErrors: []` for all 60.

Those responses were not treated as proof. Afterwards all 827 branded products were
read back from the Admin API and diffed against the intended mapping: **721 of 721
writes landed, none lost.** The only two differences were deliberate in-flight
corrections, where the live value was the correct one and the mapping file was stale.

A pass over the derived values before and during the push caught eleven that were
wrong in ways no regex would flag, because each is a real-world naming fact:

| Title | Derived | Corrected to | Why |
|---|---|---|---|
| Pallini Limoncello 70cl | Limoncello | **Pallini** | Limoncello is the category, not the producer |
| Seventy One Gin Signature **Martini** Gift Set | Martini | **Seventy One Gin** | The cocktail, not Martini & Rossi |
| Brewdog Punk IPA | Brewdog | **BrewDog** | House capitalisation |
| Passoã Passion Fruit Liqueur | Passoa | **Passoã** | The brand's own spelling |
| G.H.Mumm Rose NV Brut | Mumm | **G.H. Mumm** | Truncated at the full stop |
| Au Green Watermelon Vodka (×2) | Au | **AU Vodka** | Truncated; AU Vodka is the full mark |
| Croe Imperial Beluga Caviar | Beluga | **Croe** | Beluga is the sturgeon, not the vodka |
| Cut Caviar Royal Beluga | Beluga | **Cut Caviar** | As above |
| Caviar House Finest Beluga Caviar (×2) | Beluga | **Caviar House** | As above |
| Domaine Evremond Classic Cuvee | Domaine Evremond Classic Cuvee | **Domaine Evremond** | "Classic Cuvée" is the wine |
| Chateau Latour Les Forts de Latour 2000 | Château Latour Les Forts | **Château Latour** | Les Forts is Latour's second wine |
| Château Cos d'Estournel | Château Cos | **Château Cos d'Estournel** | Stopped at the lowercase `d'` |

The Beluga cases are the instructive ones: the same token is a vodka brand on five
products and a species of sturgeon on four others in the same catalogue. Both readings
are defensible from the title alone, so the product descriptions decided it. "The Beluga
Hamper" kept **Beluga**, because its description says it is built around Beluga Gold
Line vodka.

Earlier estate-matcher corrections are recorded above; together with these, 36 of the
721 values were set or corrected by hand rather than derived.

---

## 2026-09-18 — Brand backfill round 2

Store-wide vendor state before: **622 of 1,449** products still carried `Drinks House 247`
as the vendor (445 active, 177 draft/archived). Filter validated with a nonsense control
(`vendor:'Zzqq Not A Real Vendor'` → 0).

### Result

**225 products given a real brand. 622 → 397 remaining**, verified by re-query.

### Why only 225 and not 622

Two honest limits, both discovered by inspecting output rather than trusting the extractor:

**1. A large share legitimately has no brand.** 102 products are house or generic items —
Cranberry Juice, Tonic Water, Pack of Ice Cubes, Service Fee, Cheese Platter, the Pre-Mixed
Cases, celebration cakes, hampers. For these `Drinks House 247` is the *correct* vendor.
Inventing a brand would be worse than leaving them.

**2. Title-prefix extraction is unsafe for fine wine.** Burgundy and Bordeaux name bottles
`<Appellation> <Producer> <Vintage>`, so a naive prefix grabs the appellation:

| Title | Naive prefix | Actual brand |
|---|---|---|
| Chassagne Montrachet Bachelet Monnot 2021 | "Chassagne Montrachet Bachelet Monnot" | Bachelet-Monnot |
| Bourgogne Chardonnay Thierry Pillot 2021 | "Bourgogne Chardonnay Thierry Pillot" | Thierry Pillot |
| Chambertin Clos de Beze Armand Rousseau 1993 | "Chambertin Clos de Beze" | Armand Rousseau |
| Chablis Montee de Tonnerre Samuel Billaud | "Montee de Tonnerre Samuel" | Samuel Billaud |

The tell that the first pass was wrong: **389 of 622 derived brands appeared exactly once.**
Real brands repeat.

### Method that was actually used

1. Strip leading appellation/grape using a ~180-entry vocabulary (Burgundy villages, Bordeaux
   communes, Rhône, Italy, Spain, New World, plus grape names).
2. Match against the **274 brands already live in the store** — highest confidence.
3. Explicit estate prefixes (`Château`/`Domaine`/`Bodega`/`Quinta`/`Clos`/`Mas`/`Viña`), with a
   token-taker that carries articles through (an earlier version truncated
   "Château Le Crock" → "Château Le" and "Domaine de Montille" → "Domaine de").
4. Bordeaux shorthand: a 40-estate list mapping `Canon Magnum 2019` → `Château Canon`.
5. **Corroboration gate** — push only if the candidate matches a live brand, is an explicit
   estate, is known Bordeaux shorthand, or appears on ≥2 products.
6. **Ambiguity gate** — reject a bare fragment shared by 2+ real brands. `Heidsieck` alone
   was rejected because Charles Heidsieck, Piper-Heidsieck and Heidsieck & Co. Monopole are
   three different houses.
7. Final validation rejected candidates ending on an article (`Chateau de`), generic
   descriptors (`Mixed Fruit` from "Mixed Fruit Cider"), and anything under 3 characters.

Nine further errors were caught by eye in the generated batches and hand-corrected before
pushing (Burgundy *climats* read as producers, `Ten Minutes` → `Ten Minutes by Tractor`,
`LOUIS XIII` casing inconsistent across four products, `Château Haut-Brion Bordeaux-Blend`,
`Château de Fargues Lur Saluces Semillon-Sauvignon`, `Domaines Ott's Cuvée` → `Domaines Ott`).
Two products naming the Saint-Aubin climat *Murgers des Dents de Chien* were deferred rather
than guessed.

### Remaining

`seo/aeo/bulk/brand-backfill-round2.csv` — all 622 rows with proposed vendor, confidence and
evidence:

| Bucket | Count | Action |
|---|---|---|
| Pushed | 225 | done |
| Needs review | 289 | a proposed brand is given, but unverified |
| Leave as Drinks House 247 | 102 | house/generic — correct as-is |

The 289 are mostly single-occurrence wine producers where the appellation/climat boundary is
genuinely ambiguous without a reference list. They are worth a pass by someone who knows the
range; the CSV is ordered so that can be done quickly.
