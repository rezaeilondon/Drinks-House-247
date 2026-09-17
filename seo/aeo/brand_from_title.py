#!/usr/bin/env python3
"""Derive a product's real brand (Shopify `vendor`) from its title.

Shopify maps `vendor` to `brand` in every shopping and agentic feed. On this store it
reads "Drinks House 247" -- the retailer -- on 1,253 of 1,257 active products, which
makes every listing unmatchable against a known product catalogue.

This is deliberately HIGH PRECISION, NOT high coverage. A wrong brand is worse than no
brand: it mismatches the product against someone else's catalogue entry. Anything this
cannot identify confidently is left alone and reported for a human to handle.

Two matchers, tried in order:

1. CURATED  -- an explicit list of producers, matched longest-name-first so
   "Johnnie Walker Blue Label" cannot be shadowed by a shorter entry, and anchored to a
   word boundary so "Au" cannot match inside "Australia".

2. ESTATE   -- French/Italian estate naming, where the estate IS the brand:
   "Château Larose Trintaudon" -> "Château Larose Trintaudon".
   Only fires at the START of a title, and only consumes capitalised words, so
   "Château Haut-Blanville Merlot 75cl" stops before "Merlot".

Regional and varietal words are explicitly excluded, because "Bourgogne Chardonnay" and
"Puligny Montrachet" are appellations, not producers.
"""
import re, unicodedata

# --- words that are never a brand, used to stop the ESTATE matcher -------------
STOP = {
    # varietals
    'chardonnay','merlot','malbec','syrah','shiraz','tempranillo','sangiovese',
    'cabernet','sauvignon','blanc','noir','pinot','grigio','gris','riesling',
    'nebbiolo','garnacha','grenache','carignan','viognier','albarino','albariño',
    'chenin','zinfandel','primitivo','barbera','dolcetto','gamay','semillon',
    'verdejo','vermentino','pecorino','montepulciano','corvina','mourvedre',
    # appellations / regions
    'bourgogne','bordeaux','rioja','chablis','meursault','puligny','montrachet',
    'chassagne','margaux','medoc','médoc','pauillac','saint','sancerre','provence',
    'champagne','prosecco','rhone','rhône','beaujolais','chianti','barolo',
    'barbaresco','toscana','veneto','piemonte','languedoc','roussillon','alsace',
    'loire','douro','rueda','ribera','duero','mendoza','marlborough','stellenbosch',
    'pomerol','sauternes','cotes','côtes','coteaux','cru','grand','premier',
    'montagny','emilion','émilion','montagne','givry','mercurey','rully','pouilly',
    'fuisse','fuissé','macon','mâcon','nuits','vosne','gevrey','morey','volnay',
    'pommard','savigny','aloxe','corton','vougeot','romanee','romanée','fume','fumé',
    'michelle','ste','st','sud','haut','bas','clos','vieux','vieilles','vignes',
    'pessac','leognan','léognan','listrac','moulis','fronsac','castillon','lalande',
    'barsac','graves','entre','mers','blaye','bourg','fleurie','morgon','brouilly',
    'mireille','tondonia','crozes','hermitage','cornas','condrieu','gigondas',
    'jeroboam','methuselah','balthazar','nebuchadnezzar','salmanazar','piccolo',
    'magnum','double','litre','litres','bottle','bottles',
    # descriptors
    'reserva','reserve','riserva','gran','vintage','brut','rose','rosé','sec','demi',
    'extra','old','year','years','single','malt','blended','scotch','whisky','whiskey',
    'vodka','gin','rum','tequila','mezcal','cognac','brandy','liqueur','beer','lager',
    'cider','wine','red','white','sparkling','dry','case','gift','box','set','magnum',
}

# --- curated producers --------------------------------------------------------
BRANDS = [
 # champagne
 "Dom Pérignon","Dom Perignon","Moët & Chandon","Moet & Chandon","Moët","Moet",
 "Veuve Clicquot","Laurent-Perrier","Laurent Perrier","Louis Roederer","Krug",
 "Bollinger","Taittinger","Pol Roger","Perrier-Jouët","Perrier Jouet","Perrier-Jouet",
 "Ruinart","Dom Ruinart","Armand de Brignac","Piper-Heidsieck","Piper Heidsieck",
 "Charles Heidsieck","Billecart-Salmon","Billecart Salmon","Mercier","Gosset",
 "Devaux","Fleur de Miraval","Rare Champagne","Lanson","Mumm","Ayala","Deutz",
 "Henriot","Bruno Paillard","Jacquart","Nicolas Feuillatte","Duval-Leroy",
 # whisky
 "Johnnie Walker","Macallan","The Macallan","Glenfiddich","Glenlivet","The Glenlivet",
 "Chivas Regal","Royal Salute","Dalmore","The Dalmore","Lagavulin","Laphroaig",
 "Talisker","Ardbeg","Oban","Balvenie","The Balvenie","Highland Park","Bowmore",
 "Bruichladdich","Bunnahabhain","Caol Ila","Cragganmore","Dalwhinnie","Glenmorangie",
 "Aberfeldy","Aberlour","Monkey Shoulder","Jack Daniel's","Jack Daniels","Jameson",
 "Bushmills","Redbreast","Proper Twelve","Bell's","Bells","Famous Grouse",
 "The Famous Grouse","Nikka","Suntory","Hibiki","Yamazaki","Hakushu","Tenjaku",
 "Woodford Reserve","Maker's Mark","Makers Mark","Buffalo Trace","Bulleit",
 "Wild Turkey","Jim Beam","Knob Creek","Four Roses","Michter's","Elijah Craig",
 "Blanton's","Sazerac","Green Spot","Yellow Spot","Teeling","Roe & Co","Slane",
 "Naked Malt","Copper Dog","Cardhu","Clynelish","Springbank","Kilchoman","Arran",
 # cognac / brandy
 "Hennessy","Rémy Martin","Remy Martin","Martell","Courvoisier","Hine","Camus",
 "Prunier","Delamain","Frapin","Bisquit","Metaxa",
 # vodka
 "Grey Goose","Belvedere","Absolut","Smirnoff","Cîroc","Ciroc","Beluga",
 "Crystal Head","Stolichnaya","Ketel One","Chase","Black Cow","Au",
 # gin
 "Hendrick's","Hendricks","Bombay Sapphire","Tanqueray","Gordon's","Gordons",
 "Monkey 47","Roku","Citadelle","Fifty Pounds","City of London","The Lakes",
 "Sipsmith","Beefeater","Plymouth","Whitley Neill","Brockmans","Malfy","Gin Mare",
 "Silent Pool","Bathtub","No.3","Nordés","Nordes","Star of Bombay",
 # tequila / mezcal
 "Clase Azul","Don Julio","Patrón","Patron","Gran Patrón","Casamigos","Fortaleza",
 "Sierra","Jose Cuervo","1800","Ilegal","Herradura","Espolòn","Espolon","Olmeca",
 "Tequila Rose","El Jimador","Cazcabel","Mezcal Amores","Del Maguey","Volcan",
 "Volcán","Komos","Cincoro","818",
 # rum
 "Bacardi","Captain Morgan","Havana Club","Bumbu","Malibu","Kraken","The Kraken",
 "Diplomatico","Diplomático","Zacapa","Ron Zacapa","Mount Gay","Appleton",
 "Plantation","Rhum J.M","Sailor Jerry","Dead Man's Fingers","Koko Kanu",
 "Wray & Nephew","Doorly's","Pusser's","Goslings",
 # liqueur / aperitif
 "Baileys","Disaronno","Jägermeister","Jagermeister","Cointreau","Grand Marnier",
 "Aperol","Campari","Martini","Pimm's","Pimms","Tia Maria","Kahlúa","Kahlua",
 "Amaretto","Chambord","St-Germain","Luxardo","Fernet-Branca","Suze","Pallini",
 "Limoncello","Drambuie","Southern Comfort","Archers","Sourz","Passoa",
 # beer / cider
 "Corona","Heineken","Peroni","Stella Artois","Kronenbourg","Guinness","Asahi",
 "Madrí","Madri","Budweiser","Carlsberg","Birra Moretti","Estrella","San Miguel",
 "Tiger","Sapporo","Brewdog","Camden","Beavertown","Strongbow","Kopparberg",
 "Rekorderlig","Magners","Bulmers","Thatchers","Einstök","Einstok","Modelo",
 "Desperados","Sol","Amstel","Staropramen","Grolsch","Pilsner Urquell",
 # sparkling / other wine houses
 "Luc Belaire","Belaire","Della Vite","Freixenet","Codorníu","Codorniu",
 "Chandon","Ferrari","Bottega","Canti","San Vito","Zonin","Mionetto",
 "Villa Maria","Cloudy Bay","Oyster Bay","Whispering Angel","Miraval",
 "Whispering","Chateau d'Esclans","Château d'Esclans","Casillero Del Diablo",
 "Louis Latour","Louis Jadot","Gaja","Antinori","Tignanello","Sassicaia",
 "Ornellaia","Masi","Ruffino","Frescobaldi","Terras Gauda","Torres",
 "Marques de Riscal","Marqués de Riscal","Campo Viejo","Faustino","CVNE",
 "López de Heredia","R. López de Heredia","Vega Sicilia","Pingus","Muga",
 "Penfolds","Jacob's Creek","Hardys","Wolf Blass","Yellow Tail","19 Crimes",
 "Robert Oatley","Southern Right","The Chocolate Block","Gran Sasso",
 "Flechas de Los Andes","Calvet","Delagrave","Seguin","Baron de Badassière",
 "Kylie Minogue","Barefoot","Blossom Hill","Echo Falls","I Heart",
 # chocolate / food
 "Charbonnel et Walker","Charbonnel","Pierre Marcolini","Lindt","Ferrero Rocher",
 "Godiva","Hotel Chocolat","Green & Black's","Pringles","Haribo","M&M","Nurofen",
 # soft / mixers
 "Red Bull","Redbull","Coca-Cola","Coke","Schweppes","Fever-Tree","Fever Tree",
 "Britvic","Fanta","Sprite","Lucozade","Evian","San Pellegrino","Perrier",
 "Highland Spring","Volvic","Ting","Ribena","J2O","Appletiser",
]
# longest first so multi-word brands win
BRANDS = sorted(set(BRANDS), key=lambda s: (-len(s), s))


def _fold(s):
    """lowercase, strip accents, normalise quotes/dashes.

    'Moët' must match 'Moet', and a curly apostrophe in "Chateau d’Esclans" must match
    the straight one in the curated list -- that mismatch silently cost a producer match.
    """
    s = (s or '').replace('\u2019', "'").replace('\u2018', "'")
    s = s.replace('\u2013', '-').replace('\u2014', '-')
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.lower()


# One canonical spelling per producer. Feeds match on exact brand strings, so
# "Moet" and "Moët & Chandon" must not both appear across the catalogue.
CANON = {
    'Moet': 'Moët & Chandon', 'Moët': 'Moët & Chandon',
    'Moet & Chandon': 'Moët & Chandon',
    'Dom Perignon': 'Dom Pérignon',
    'Laurent Perrier': 'Laurent-Perrier',
    'Perrier Jouet': 'Perrier-Jouët', 'Perrier-Jouet': 'Perrier-Jouët',
    'Piper Heidsieck': 'Piper-Heidsieck',
    'Billecart Salmon': 'Billecart-Salmon',
    'Jack Daniels': "Jack Daniel's",
    'Hendricks': "Hendrick's", 'Gordons': "Gordon's", 'Bells': "Bell's",
    'Remy Martin': 'Rémy Martin', 'Ciroc': 'Cîroc',
    'Patron': 'Patrón', 'Gran Patrón': 'Patrón', 'Gran Patron': 'Patrón',
    'Jagermeister': 'Jägermeister', 'Kahlua': 'Kahlúa',
    'Madri': 'Madrí', 'Einstok': 'Einstök', 'Espolon': 'Espolòn',
    'Volcan': 'Volcán', 'Nordes': 'Nordés', 'Codorniu': 'Codorníu',
    'Diplomatico': 'Diplomático', 'Zacapa': 'Ron Zacapa',
    'Redbull': 'Red Bull', 'Coke': 'Coca-Cola', 'Fever Tree': 'Fever-Tree',
    'Pimms': "Pimm's", 'Makers Mark': "Maker's Mark",
    'The Macallan': 'Macallan', 'The Glenlivet': 'Glenlivet',
    'The Dalmore': 'Dalmore', 'The Balvenie': 'Balvenie',
    'The Famous Grouse': 'Famous Grouse', 'The Kraken': 'Kraken',
    'Charbonnel': 'Charbonnel et Walker',
    'Belaire': 'Luc Belaire',
    'Marques de Riscal': 'Marqués de Riscal',
    'R. López de Heredia': 'López de Heredia',
    'Chateau d\'Esclans': "Château d'Esclans",
    'Whispering': "Château d'Esclans", 'Whispering Angel': "Château d'Esclans",
    'Tignanello': 'Antinori',
}


_ESTATE = re.compile(
    r'^(Ch[aâ]teau|Domaine|Maison|Weingut|Tenuta|Bodegas?|Quinta)\s+(.+)$',
    re.I)


def brand_for(title):
    """Return (brand, how) or (None, reason)."""
    t = re.sub(r'\s+', ' ', (title or '').strip())
    if not t:
        return None, 'empty-title'
    ft = _fold(t)

    # 1. curated, word-boundary anchored
    for b in BRANDS:
        fb = _fold(b)
        if re.search(r'(?<![a-z0-9])' + re.escape(fb) + r'(?![a-z0-9])', ft):
            return CANON.get(b, b), 'curated'

    # 2. estate naming, start of title only
    m = _ESTATE.match(t)
    if m:
        head, rest = m.group(1), m.group(2)
        out = []
        ARTICLES = {'de','du','des','la','le','les','di','da','del','della','the','of','et','and'}
        for w in rest.split(' '):
            bare = w.strip(',').strip()
            if not bare:
                break
            fb = _fold(bare)
            # A hyphenated token is an appellation if ANY part is: "Chassagne-Montrachet",
            # "Montagne-Saint-Emilion". Checked part-by-part or these slip through whole.
            parts = [x for x in re.split(r'[-\u2013\u2014]', fb) if x]
            if fb in STOP or any(x in STOP for x in parts):
                break
            if fb in ARTICLES and out:
                out.append(bare); continue
            if fb in ARTICLES and not out:
                break
            # A vintage year or a bottle size is never part of a producer's name:
            # "Château Latour 2008 75cl" -> "Château Latour".
            if re.fullmatch(r'\d{4}', bare) or re.fullmatch(r'\d+(cl|l|ml|L)', bare, re.I):
                break
            if bare[0].isdigit():
                break
            if not bare[0].isupper():
                break
            out.append(bare)
            if len(out) == 3:
                break
        if out:
            head = 'Château' if _fold(head).startswith('chateau') else head.title()
            return f'{head} ' + ' '.join(out).rstrip(','), 'estate'

    return None, 'no-confident-match'
