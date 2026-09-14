import json, re, html

SITE = "https://www.drinkshouse247.co.uk"
QA = []          # (section, question, answer_html)
BLOCKS = []      # ordered page body pieces

def qa(section, q, a):
    QA.append((section, q, a))

def strip(h):
    t = re.sub(r"<[^>]+>", "", h)
    return html.unescape(re.sub(r"\s+", " ", t)).strip()

# ---------------- DELIVERY & SERVICE ----------------
S = "Delivery and service"
qa(S, "Can you get alcohol delivered at 3am in London?",
   "Yes. Drinks House 247 delivers alcohol across London 24 hours a day, 365 days a year, "
   "typically within 30–45 minutes of ordering. There is no cut-off time: an order placed at "
   "3am is handled exactly like one placed at 3pm. The person receiving it must be 18 or over "
   "and may be asked for ID at the door.")
qa(S, "Do you need ID for alcohol delivery in the UK?",
   "Yes. UK retailers must verify that the recipient is 18 or over, and the check happens at "
   'the door rather than at checkout. Drinks House 247 operates a <a href="/pages/challenge-21">Challenge 21</a> '
   "policy, so if the person accepting the delivery looks under 21 the driver will ask for photo ID. "
   "A passport, UK driving licence or PASS-accredited card is accepted. Without ID, the driver cannot "
   "hand the order over.")
qa(S, "Can alcohol be delivered to a hotel in London?",
   "Yes, and it is one of the most common requests in central London. Add the guest's full name and "
   "room number to the delivery address so reception can route it correctly. Many hotels ask that "
   "deliveries are left with the concierge, in which case a staff member over 18 signs for it. "
   'Same-day delivery covers <a href="/pages/alcohol-delivery-areas">every London borough inside the M25</a>.')
qa(S, "Can you send alcohol as a gift to someone else's address?",
   "Yes. Enter the recipient's address at checkout rather than your own and add a gift note, which is "
   "included with the order. Whoever opens the door must be 18 or over and may be asked for ID, so it "
   "is worth telling the recipient to expect a delivery. London orders arrive the same day; the rest of "
   'UK mainland is next day. Browse <a href="/collections/champagne-gifts">champagne gifts</a> or '
   '<a href="/collections/alcohol-gift-sets">gift sets and hampers</a>.')
qa(S, "What happens if nobody is home when alcohol is delivered?",
   "Alcohol cannot be left on a doorstep, with a neighbour or in a safe place, because the age check "
   "has to happen in person. If nobody answers, the driver will attempt to call the number on the order. "
   "If they still cannot hand it over, the order returns to base and a redelivery is arranged. Adding a "
   "working mobile number at checkout is the single best way to avoid this.")
qa(S, "How fast is alcohol delivery in London, realistically?",
   "Most central and inner London deliveries land in 30–45 minutes from the Battersea base. Outer "
   "boroughs and the edges of the M25 can take longer, and Friday and Saturday nights are the busiest "
   "windows. Order size makes little difference to speed; distance and time of night make the most. "
   'For time-critical orders, see <a href="/pages/instant-alcohol-delivery">instant alcohol delivery</a>.')
qa(S, "Can you get alcohol delivered on Christmas Day?",
   "Yes. Drinks House 247 operates every day of the year, including Christmas Day, Boxing Day and New "
   "Year's Day, when most shops and supermarkets are shut. Demand is far higher than normal on those "
   "dates, so delivery windows stretch — ordering earlier in the day is sensible rather than essential.")
qa(S, "How late can you buy alcohol in London?",
   "Shop licensing hours vary by borough, and most off-licences stop selling somewhere between 11pm "
   "and 1am. Licensed delivery services are not bound by the same shop-front hours, which is why "
   "delivery is usually the only option after midnight. If you are searching for a shop rather than "
   'a delivery, see <a href="/pages/off-license-near-me-london">24-hour off-licences in London</a>.')

BLOCKS.append(("html", """
<h2 id="delivery">Delivery and service</h2>
<p>These are the practical questions people ask most often about getting alcohol delivered in London.</p>
"""))

# ---------------- CHAMPAGNE ----------------
S2 = "Champagne"
qa(S2, "How many glasses are in a bottle of champagne?",
   "A standard 75cl bottle pours six 125ml flutes. Poured more generously, or into wider coupes, expect "
   "five. For a single welcome toast, one bottle serves six to eight people because glasses are filled "
   "less full. Magnums (1.5L) give twelve flutes and are the usual choice for a top table.")
qa(S2, "How much champagne do I need for 50 guests?",
   "For a welcome toast only, allow one bottle per six guests — about nine bottles for 50 people. If "
   "champagne is being drunk through the evening rather than just raised once, allow half a bottle per "
   "adult, which is 25 bottles for 50 guests. Add roughly 10% so you do not run out at the wrong moment.")
qa(S2, "What temperature should champagne be served at?",
   "Serve non-vintage champagne at 8–10°C and vintage or prestige cuvées slightly warmer at 10–12°C, "
   "where more of the aroma comes through. That means about three hours in the fridge, or 20–30 minutes "
   "in a bucket of half ice, half water. Serving it near freezing mutes everything you paid for.")
qa(S2, "How long does champagne last once opened?",
   "With a proper sparkling-wine stopper, an opened bottle keeps its mousse for three to five days in "
   "the fridge. Without one, it is noticeably flat within a day. The teaspoon-in-the-neck trick does "
   "nothing; what actually helps is keeping the bottle cold, because carbon dioxide stays dissolved "
   "more readily at low temperatures.")
qa(S2, "How long does unopened champagne last?",
   "Non-vintage champagne is made to be drunk on release and is at its best within three to four years. "
   "Vintage and prestige cuvées can improve for a decade or more. Store bottles on their side, away from "
   "light, at a stable 10–14°C. Heat and temperature swings do far more damage than age itself.")
qa(S2, "What is the difference between champagne and sparkling wine?",
   "Champagne is a protected name: only sparkling wine made in the Champagne region of France, using the "
   "traditional method of a second fermentation in the bottle, may use it. Prosecco, cava, crémant and "
   "English sparkling wine are made elsewhere, and prosecco usually ferments in a tank rather than the "
   "bottle, which gives a lighter, more fruit-forward style.")
qa(S2, "What does Blanc de Blancs mean?",
   "Blanc de Blancs means the wine is made entirely from white grapes — in Champagne, that is Chardonnay. "
   "Blanc de Noirs is white wine made from black grapes, Pinot Noir and Pinot Meunier. Blanc de Blancs "
   "tends to be lighter, crisper and more citrus-driven; Blanc de Noirs is broader and more red-fruited. "
   'Browse <a href="/collections/blanc-de-blancs-champagne">Blanc de Blancs</a> and '
   '<a href="/collections/blanc-de-noirs-champagne">Blanc de Noirs</a>.')
qa(S2, "Is expensive champagne actually better?",
   "Up to a point, yes: higher prices usually buy longer ageing on the lees, a greater share of reserve "
   "wines and fruit from better-rated villages, all of which show in the glass. Beyond roughly £150 a "
   "bottle you are increasingly paying for rarity, packaging and name recognition rather than a "
   "proportionate jump in quality. For a gift, recognition genuinely matters; for drinking, it often does not.")

BLOCKS.append(("html", """
<h2 id="champagne">Champagne</h2>
<p>Serving, storing and choosing — the questions that decide whether a good bottle shows well.</p>
<h3>Champagne bottle sizes and servings</h3>
<div style="overflow-x:auto">
<table>
<thead><tr><th>Format</th><th>Capacity</th><th>125ml flutes</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td>Quarter / Piccolo</td><td>20cl</td><td>1–2</td><td>Single serve, favours</td></tr>
<tr><td>Half</td><td>37.5cl</td><td>3</td><td>Two people, tasting</td></tr>
<tr><td>Standard</td><td>75cl</td><td>6</td><td>Everyday and gifting</td></tr>
<tr><td>Magnum</td><td>1.5L</td><td>12</td><td>Top table, ages more slowly</td></tr>
<tr><td>Jeroboam</td><td>3L</td><td>24</td><td>Large parties, display</td></tr>
<tr><td>Methuselah</td><td>6L</td><td>48</td><td>Events, statement piece</td></tr>
</tbody>
</table>
</div>
<p>Shop by format: <a href="/collections/champagne-half-bottle-37-5cl">half bottles</a>,
<a href="/collections/champagne-standard-bottle-75cl">standard 75cl</a>,
<a href="/collections/champagne-jeroboam-3l">jeroboams</a>, or browse
<a href="/collections/champagne">all champagne</a>.</p>
"""))

# ---------------- WINE ----------------
S3 = "Wine"
qa(S3, "How long does opened wine last?",
   "Light whites and rosés hold up for two to three days in the fridge; fuller reds for three to five "
   "days re-corked and kept cool. Fortified wines like port and sherry last weeks. What kills wine is "
   "oxygen, so the emptier the bottle, the faster it fades — decanting leftovers into a smaller bottle "
   "buys you an extra day or two.")
qa(S3, "What temperature should red wine be served at?",
   "Most red wine shows best between 14°C and 18°C, which is cooler than a typical heated UK room. "
   "Lighter reds such as Beaujolais or young Pinot Noir are better at the bottom of that range and "
   "benefit from 20 minutes in the fridge. Served at 22°C, alcohol dominates and fruit flattens out.")
qa(S3, "How many units are in a bottle of wine?",
   "A 75cl bottle at 12% ABV contains 9 UK units; at 13.5% it is about 10 units, and at 14% it is 10.5. "
   "The formula is ABV multiplied by volume in litres. UK guidance is to drink no more than 14 units a "
   "week, spread across several days — roughly a bottle and a half of average-strength wine.")
qa(S3, "Do you need to decant wine?",
   "Decanting does two different jobs: separating an older wine from its sediment, and aerating a young, "
   "tight wine so it opens up. Young structured reds such as Bordeaux, Barolo or Syrah benefit from "
   "30–60 minutes. Delicate older wines can fall apart with too much air, so decant those gently and "
   "serve promptly. Most everyday wine needs nothing more than time in the glass.")
qa(S3, "How many bottles of wine per person at a wedding?",
   "Plan half a bottle per adult guest across a seated meal, rising to about three-quarters of a bottle "
   "for a long reception with no other drinks on offer. For 100 guests that is roughly 50 bottles as a "
   "baseline and 75 for a full evening. Split it around 60% white and rosé to 40% red for a summer "
   "wedding, and reverse that in winter.")

BLOCKS.append(("html", """
<h2 id="wine">Wine</h2>
<p>Serving, storing and quantity questions for wine — see also our
<a href="/pages/checklist-for-storing-wine-at-home-safely">home wine storage checklist</a>.</p>
"""))

# ---------------- SPIRITS ----------------
S4 = "Spirits"
qa(S4, "What is the difference between mezcal and tequila?",
   "Both are agave spirits from Mexico. Tequila must be made from blue weber agave, grown in Jalisco and "
   "parts of four neighbouring states, and the agave is usually steamed in ovens. Mezcal can be made from "
   "dozens of agave varieties and is traditionally roasted in earth pits over hot rocks, which is where "
   "its smoke comes from. All tequila is technically a type of mezcal; the reverse is not true.")
qa(S4, "Why is Clase Azul tequila so expensive?",
   "A large share of the price is the bottle. Each Clase Azul decanter is hand-made and hand-painted by "
   "artisans in Santa María Canchesdá, Mexico, and no two are identical. The tequila itself is slow-cooked "
   "agave aged in oak, produced in small volumes. You are buying a decorative object as much as a spirit, "
   'which is why it gifts so well. See the <a href="/collections/clase-azul-tequila">Clase Azul range</a>.')
qa(S4, "What is cristalino tequila?",
   "Cristalino is añejo or extra añejo tequila that has been charcoal-filtered to strip out the colour "
   "picked up from the barrel while keeping much of the vanilla and oak character. The result looks like "
   "a blanco but tastes aged and noticeably smoother. Purists object that filtration removes character; "
   "in practice it has become one of the fastest-growing categories in premium tequila.")
qa(S4, "What do VS, VSOP and XO mean on cognac?",
   "They are minimum ages for the youngest eau-de-vie in the blend. VS is at least two years, VSOP at "
   "least four, and XO at least ten. Older blends are rounder and more dried-fruit driven, younger ones "
   "brighter and better in cocktails. The grade tells you nothing about the oldest component, which is "
   'often far older. Browse <a href="/collections/cognac">cognac</a>.')
qa(S4, "How long do opened spirits last?",
   "Unopened, spirits keep more or less indefinitely if stored upright and out of sunlight. Once opened, "
   "expect one to two years before oxidation noticeably dulls the flavour, and faster as the bottle empties "
   "and air fills the space. A bottle with an inch left will fade within months, which is an argument for "
   "finishing it rather than saving it.")
qa(S4, "Should you refrigerate tequila, whisky or gin?",
   "Spirits are shelf-stable and do not need refrigeration. Chilling mutes aroma, so sipping spirits — good "
   "añejo tequila, single malt, aged rum — are best at room temperature. Vodka and some gins are pleasant "
   "straight from the freezer, where the cold thickens the texture. Store everything upright: high-strength "
   "spirit degrades corks over time.")

BLOCKS.append(("html", """
<h2 id="spirits">Spirits</h2>
<p>Agave, cognac and storage questions. Browse
<a href="/pages/whisky-delivery-london">whisky</a>,
<a href="/pages/tequila-delivery-london">tequila</a>,
<a href="/pages/gin-delivery-london">gin</a>,
<a href="/pages/vodka-delivery-london">vodka</a>,
<a href="/pages/rum-delivery-london">rum</a> and
<a href="/pages/cognac-delivery-london">cognac</a>.</p>
"""))

# ---------------- QUANTITIES ----------------
S5 = "Quantities and planning"
qa(S5, "How many drinks does a bottle of spirits make?",
   "A 70cl bottle yields 28 single 25ml measures, or 14 doubles. A 1L bottle gives 40 singles. For "
   "cocktails, assume a 50ml pour, which gives 14 drinks from a 70cl bottle. When planning a party, "
   "count spirits in drinks rather than bottles — it is the only way the numbers work.")
qa(S5, "How much alcohol do I need for a party of 100?",
   "A workable starting point is two drinks per guest in the first hour and one per hour after. For 100 "
   "guests over four hours that is around 500 drinks. Split roughly 40% wine, 30% beer, 20% spirits and "
   "10% soft drinks, then adjust for the crowd. Always over-order soft drinks and ice — both run out first.")
qa(S5, "How much ice do you need for a party?",
   "Allow about 1kg of ice per guest for a party where drinks are being mixed, and more in summer. Ice "
   "does two jobs — chilling bottles and going into glasses — and people routinely buy enough for only "
   "the second. For spirits served over a single large cube, less is needed but it must be better quality.")
qa(S5, "How far in advance should you order drinks for an event?",
   "For a large wedding, order six to eight weeks ahead so quantities and any special bottles can be "
   "confirmed. Corporate events need about two weeks. In London, same-day delivery means genuine "
   "last-minute orders are still possible — but around Christmas and New Year, demand is high enough "
   "that ordering ahead is worth the small effort.")

BLOCKS.append(("html", """
<h2 id="quantities">Quantities and planning</h2>
<h3>Drinks per bottle, at a glance</h3>
<div style="overflow-x:auto">
<table>
<thead><tr><th>Bottle</th><th>Size</th><th>Servings</th><th>Serving size</th></tr></thead>
<tbody>
<tr><td>Champagne / sparkling</td><td>75cl</td><td>6</td><td>125ml flute</td></tr>
<tr><td>Wine</td><td>75cl</td><td>5</td><td>150ml glass</td></tr>
<tr><td>Wine (small pours)</td><td>75cl</td><td>6</td><td>125ml glass</td></tr>
<tr><td>Spirits</td><td>70cl</td><td>28 / 14</td><td>25ml single / 50ml double</td></tr>
<tr><td>Spirits</td><td>1L</td><td>40 / 20</td><td>25ml single / 50ml double</td></tr>
</tbody>
</table>
</div>
"""))


KEEP = {
 "Can you get alcohol delivered at 3am in London?",
 "Do you need ID for alcohol delivery in the UK?",
 "Can alcohol be delivered to a hotel in London?",
 "Can you send alcohol as a gift to someone else's address?",
 "What happens if nobody is home when alcohol is delivered?",
 "Can you get alcohol delivered on Christmas Day?",
 "How many glasses are in a bottle of champagne?",
 "How much champagne do I need for 50 guests?",
 "What temperature should champagne be served at?",
 "How long does champagne last once opened?",
 "How long does opened wine last?",
 "What temperature should red wine be served at?",
 "How many units are in a bottle of wine?",
 "What is the difference between mezcal and tequila?",
 "Why is Clase Azul tequila so expensive?",
 "What do VS, VSOP and XO mean on cognac?",
}
QA[:] = [t for t in QA if t[1] in KEEP]
assert len(QA) == len(KEEP), (len(QA), len(KEEP))

# ---------------- build body ----------------
def section_html(title):
    out = []
    for sec, q, a in QA:
        if sec != title:
            continue
        out.append(f"<h3>{html.escape(q)}</h3>\n<p>{a}</p>")
    return "\n".join(out)

body = []
body.append("<h1>Alcohol, Champagne and Wine Delivery in London: Your Questions Answered</h1>")
body.append(
    "<p><strong>Drinks House 247 is a 24-hour alcohol delivery service in London, delivering champagne, "
    "wine, spirits and beer across the capital in 30&ndash;45 minutes, every day of the year, with next-day "
    "delivery to the rest of UK mainland.</strong> This page answers the questions we are asked most often "
    "&mdash; about delivery rules, serving, storage and quantities &mdash; in plain terms, without the sales pitch.</p>"
)
body.append(
    '<p>Every answer below is written to be useful on its own. If you already know what you want, go '
    'straight to <a href="/collections/champagne">champagne</a>, '
    '<a href="/collections/best-sellers">best sellers</a> or '
    '<a href="/collections/alcohol-gift-sets">gift sets and hampers</a>.</p>'
)

# contents
secs = [("Delivery and service","delivery"),("Champagne","champagne"),("Wine","wine"),
        ("Spirits","spirits"),("Quantities and planning","quantities")]
body.append("<h2>On this page</h2>\n<ul>" + "".join(
    f'<li><a href="#{sid}">{html.escape(s)}</a></li>' for s, sid in secs) + "</ul>")

order = {"Delivery and service":0,"Champagne":1,"Wine":2,"Spirits":3,"Quantities and planning":4}
for (s, sid), (kind, blk) in zip(secs, BLOCKS):
    body.append(blk.strip())
    body.append(section_html(s))

body.append("""
<h2 id="order">Ordering from Drinks House 247</h2>
<p>London orders are delivered the same day, around the clock, from our Battersea base to every borough
inside the M25. Orders outside London are sent next day to UK mainland addresses. Add a gift note at
checkout if you are sending to someone else, and include a mobile number so the driver can reach the
recipient.</p>
<p>We operate a <a href="/pages/challenge-21">Challenge 21</a> policy: whoever accepts the delivery must be
18 or over, and photo ID may be requested. Please drink responsibly.</p>
<p>Questions we have not answered here? Call <strong>0203 4883266</strong>, email
<a href="mailto:sales@drinkshouse247.co.uk">sales@drinkshouse247.co.uk</a>, or see our
<a href="/pages/contact-us">contact page</a>. For coverage by area, see
<a href="/pages/alcohol-delivery-areas">the areas we deliver to</a>.</p>
<p><a href="/collections/champagne"><strong>&rarr; Browse champagne</strong></a> &nbsp;|&nbsp;
<a href="/pages/alcohol-delivery"><strong>&rarr; 24-hour alcohol delivery</strong></a></p>
""".strip())

# ---------------- JSON-LD ----------------
faq = {
    "@type": "FAQPage",
    "@id": f"{SITE}/pages/alcohol-delivery-london-questions-answered#faq",
    "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
        for _, q, a in QA
    ],
}
biz = {
    "@type": "LocalBusiness",
    "@id": f"{SITE}#business",
    "name": "Drinks House 247",
    "description": "24-hour alcohol, champagne, wine and spirits delivery service in London, "
                   "with same-day delivery across the capital and next-day delivery UK-wide.",
    "url": SITE,
    "telephone": "+442034883266",
    "email": "sales@drinkshouse247.co.uk",
    "priceRange": "££-££££",
    "currenciesAccepted": "GBP",
    "address": {"@type": "PostalAddress", "addressLocality": "London",
                "addressRegion": "Greater London", "addressCountry": "GB"},
    "areaServed": [{"@type": "City", "name": "London"},
                   {"@type": "Country", "name": "United Kingdom"}],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "00:00", "closes": "23:59",
    }],
}
web = {
    "@type": "WebPage",
    "@id": f"{SITE}/pages/alcohol-delivery-london-questions-answered",
    "name": "Alcohol, Champagne and Wine Delivery in London: Your Questions Answered",
    "description": "Straight answers on London alcohol delivery, age verification, champagne "
                   "serving and storage, wine, spirits and party quantities.",
    "isPartOf": {"@id": f"{SITE}#business"},
    "about": {"@id": f"{SITE}#business"},
}
ld = {"@context": "https://schema.org", "@graph": [biz, web, faq]}

body.append('<script type="application/ld+json">\n'
            + json.dumps(ld, ensure_ascii=False, separators=(",",":")) + "\n</script>")

out = "\n\n".join(body)
open("/tmp/landing_body.html", "w", encoding="utf-8").write(out)

# validate
assert json.loads(json.dumps(ld))
print("Q&As:", len(QA))
print("body chars:", len(out))
print("JSON-LD entities:", [e["@type"] for e in ld["@graph"]])
print("FAQ entries in schema:", len(faq["mainEntity"]))
for _, q, a in QA:
    assert strip(a), q
    assert len(strip(a).split()) >= 30, f"too short: {q}"
print("all answers >=30 words: OK")
