# Phrase Match Example Bank

Every pair the guideline states, verbatim, with its own note where one is given. Pairs are written `keyword → query`. This is the calibration set: when a live pair resembles one of these, the guideline has already decided it and your reasoning does not outrank it.

## Contents

- [Good](#good) · [Acceptable](#acceptable) · [Bad](#bad)
- [Special cases](#special-cases)
- [Pairs that look alike and rate differently](#pairs-that-look-alike-and-rate-differently)

## Good

### Intent enhancement — keyword's intent plus beneficial specificity

| Keyword → Query | Note |
|---|---|
| `restaurant` → `sushi restaurant` | same intent + cuisine detail |
| `pharmacy` → `24-hour pharmacy` | same intent + availability |
| `chicken` → `fried chicken` | same food + preparation method |
| `dentist` → `emergency dentist` | same service + urgency |
| `hotel` → `pet-friendly hotel` | same category + beneficial attribute |
| `pizza` → `chicago deep dish pizza` | same food + style/location detail |

### Semantic equivalents — clear synonyms, minimal ambiguity

| Keyword → Query | Note |
|---|---|
| `auto repair` → `car repair` | automobile vs car — same meaning |
| `auto repair` → `repair auto` | same service, token reordering |
| `coffee shop` → `coffee house` | shop vs house — clear business synonyms |
| `gas pump` → `petrol pump` | regional language variations |
| `pretty dress` → `beautiful dress` | clear synonym adjectives |
| `lux hotels` → `luxury hotel` | abbreviation to full form — **see `resolved-tensions.md`** |

### The numbered Good table

| # | Keyword | Query | Note |
|---|---|---|---|
| 1 | pizza delivery | pizza delivery near me | Same service, adds proximity |
| 2 | dentist | emergency dentist | More narrow category |
| 3 | starbucks | starbucks nyc | Same brand, adds geo intent |
| 4 | restaurant | sushi restaurant | More narrow category |
| 5 | pharmacy | 24 hour pharmacy | Same category, added attribute |
| 6 | coffee shop | coffee house | Full containment, synonym variation |
| 7 | walmart | walmart supercenter | Full containment, brand variation |
| 8 | dining | fine dining | More narrow category |
| 9 | dining | outdoor dining | Same category, added attribute |
| 10 | dining | waterfront dining | Same category, added attribute |

## Acceptable

### Intent contained, but the advertiser might be surprised

| Keyword → Query | Note |
|---|---|
| `church` → `churchs chicken` | religious intent vs restaurant brand |
| `apple` → `apple bee` | fruit or tech brand vs restaurant brand |
| `beach` → `palm beach outlets` | natural location vs shopping destination |

### Closely related, with interpretive differences

| Keyword → Query | Note |
|---|---|
| `luxury hotel` → `five star hotel` | subjective luxury vs rating system classification |
| `fitness studio` → `fitness center` | studio implies smaller/specialized vs center implies larger/general |
| `wedding photographer` → `wedding photo` | service provider vs product ambiguity |
| `vegan food` → `plant based food` | dietary philosophy vs ingredient description |
| `hair cut` → `hair buzz` | cut implies scissors and buzz implies razor |

### The numbered Acceptable table

| # | Keyword | Query | Note |
|---|---|---|---|
| 1 | starbucks cafe | starbucks coffee shop | Different classifications for cafe and coffee shop, but likely same intent |
| 2 | fitness studio | fitness center | Different classifications for studio and center, but likely same intent |
| 3 | pizza place | pzza place | Likely typo with the same intent |
| 4 | wedding photographer | wedding photo | Service vs product ambiguity, potential for autocomplete |
| 5 | steak restaraunt | steakhouse | Close variants, uncertain if exact equivalence |
| 6 | coffee shop free wifi | coffee shop with wifi | Keyword specified free wifi, but query is likely for the same |
| 7 | church | churchs chicken | Full intent contained, advertiser may be surprised to match |
| 8 | daves hot chicken | daves hote chicken | Likely typo with the same intent |
| 9 | daves hot chicken | daves ht chicken | Likely typo with the same intent |
| 10 | daves hot chicken | dave's how chicken | Likely typo with the same intent |
| 11 | hair cut | hair buzz | Close variants, uncertain if exact equivalence |
| 12 | beach | palm beach outlets | Full intent contained, advertiser may be surprised to match |
| 13 | apple | apple bee | Full intent contained, advertiser may be surprised to match |
| 14 | apple | caramel apple | Advertiser may be surprised if intending the brand Apple and not the keyword |
| 15 | vegan food | plant based food | Close variants, uncertain if exact equivalence |
| 16 | luxury hotel | 5 star hotel | Close variants in this context. The cited definition of luxury hotel is "This category includes 5-star and above hotels, which are considered the highest level of hospitality in the industry." |
| 17 | attorney | lawyer | Different legal categories however they can be used colloquially similarly |

> Why `apple` → `apple bee` is Acceptable, in the guideline's own words: *Apple appears completely within "apple bee"; but creates ambiguity, tech company vs restaurant; Acceptable because intent IS contained, but advertiser might be surprised. In practice, negative keywords would prevent unwanted matches.*

## Bad

### Intent loss — query removes essential specificity

`sushi restaurant` → `restaurant` · `24-hour pharmacy` → `pharmacy` · `fried chicken` → `chicken`

### Intent change — fundamentally different intent

| Keyword → Query | Note |
|---|---|
| `pizza delivery` → `pizza recipes` | service vs cooking |
| `dentist` → `dental school` | healthcare vs education |
| `McDonald's` → `Burger King` | competing brands |
| `french fries` → `McDonald's` | food item vs brand |
| `thai food` → `pad thai` | category vs specific dish |
| `breakfast` → `pancakes` | meal category vs specific food |
| `car wash` → `auto detailing` | basic vs comprehensive service |
| `barber shop` → `hair salon` | different business models/demographics |
| `ice cream` → `frozen yogurt` | different dessert categories |
| `coffee` → `espresso` | different beverage preparations |

### No clear connection

`restaurant` → `grocery store` · `apple` → `orange` · `sandwich` → `turkey club` (different items, even if on same hierarchy)

### The numbered Bad table

| # | Keyword | Query | Note |
|---|---|---|---|
| 1 | pizza delivery | pizza recipes | Different intent: delivery service vs cooking |
| 2 | dentist | dental school | Different intent: healthcare vs education |
| 3 | mcdonald | burger king | Competing brands, conflicting intent |
| 4 | italian restaurant | restaurant | Loses essential cuisine specificity |
| 5 | italian restaurant | dominos pizza | Different intent, category vs chain |
| 6 | italian restaurant | pizza | Different intent, category vs keyword/category |
| 7 | 24/7 plumber | plumber | Loses essential urgency specificity |
| 8 | sushi restaurant | japanese restaurant | Loses dish specificity (sushi vs all japanese) |
| 9 | 24 hour pharmacy | pharmacy | Loses essential time availability |
| 10 | starbucks | coffee shop | Loses essential brand specificity |
| 11 | hair cut | hair removal | Different intent: cutting vs removal |
| 12 | hair cut | hair braiding | Different intent: cutting vs braiding |
| 13 | hair salon | buw human hair factory store | Different intent: salon vs purchasing human hair |
| 14 | hair spa | health spa | Different intent: hair vs health |
| 15 | womens hair cut | hair cut | Loses essential gender specificity |
| 16 | hotel | hostel | Although a potential typo, a hostel is a distinct category from a hotel |
| 17 | apple | applebees | Loses the phrase "apple" from being included in the query |

## Special cases

### Alternate spelling and misspelling

Head forms (canonical): `McDonald's` (not `McD` or `Mcdonalds`), `Starbucks` (not `Starbux` or `SB`), `Best Buy` (not `BB` or `BestBuy`).
Variant forms: abbreviations, misspellings, alternate spellings, colloquialisms — `McD`, `Mickey D's`, `Starbux`, `SBUX`.

**Good when intent preserved**

`mcd` → `mcd near me` · `mcd` → `epic mcd` · `raising cane's` → `raising canes chicken fingers` · `mcdonalds` → `mcd` (system-recognized abbreviation) · `starbucks` → `starbux` · `raising canes` → `canes`

**Bad — asymmetric alternate spelling matching**

`mcd` → `mcdonalds` (abbreviated keyword should not match full brand name query) · `starbux` → `starbucks`

**Bad when intent is unclear or different**

`mcd auto services` → `mcd apparel` · `raising cane's` → `zaxby's` · `starbucks` → `starbys` · `mcdonalds` → `mike d`

### Token reordering — Good

`chinese food delivery` → `delivery chinese food` · `auto repair` → `repair auto` · `emergency plumber` → `hire a plumber for emergency` · `pizza place` → `best place to get pizza`

> The last two show that filler words added around the keyword's tokens do not cost anything.

### Transliterations — Bad

`mcdonalds` → `麦当劳` — Bad even if meaning is equivalent across languages.

> This inverts Close Variants, where transliterations are Good. See `sibling-boundary.md`.

### Geographic enhancement vs loss

**Good:** `dining` → `waterfront dining` · `chicken` → `nashville hot chicken` · `pizza` → `pizza in downtown chicago` · `dentist` → `dentist portland oregon`

**Bad:** the exact reverse of each — `waterfront dining` → `dining`, `nashville hot chicken` → `chicken`, `pizza in downtown chicago` → `pizza`, `dentist portland oregon` → `dentist`

### Attribute enhancement vs loss

**Good:** `dining` → `fine dining` · `dining` → `outdoor dining` · `restaurant` → `restaurant open now` · `pharmacy` → `drive thru pharmacy`

**Bad:** the exact reverse of each.

### Food-specific

**Category → keyword enhancement (Good):** `chicken` → `fried chicken` · `chicken` → `hot chicken` · `chicken` → `chicken fingers`

**Keyword → category loss (Bad):** `chicken fingers` → `chicken` · `fried chicken` → `chicken` · `hot chicken` → `chicken`

**Different food items (Bad):** `chicken fingers` → `chicken salad` · `fried chicken` → `chicken soup`

The guideline's reasoning: *someone searching "chicken fingers" wants that exact item; someone searching "chicken" might want any chicken dish.* And `fruit` → `apple` is **Bad** because fruit could mean oranges, bananas, etc.

## Pairs that look alike and rate differently

These are the calibration traps. Each row is two guideline-stated pairs that differ by one small thing.

| Pair A | Pair B | What separates them |
|---|---|---|
| `apple` → `apple bee` — **Acceptable** | `apple` → `applebees` — **Bad** | A space. The keyword must survive as a token, not a character run |
| `restaurant` → `sushi restaurant` — **Good** | `sushi restaurant` → `restaurant` — **Bad** | Direction |
| `chicken` → `chicken fingers` — **Good** | `sandwich` → `turkey club` — **Bad** | Whether the keyword's own word survives in the query |
| `mcdonalds` → `mcd` — **Good** | `mcd` → `mcdonalds` — **Bad** | Head form must be the keyword, not the query |
| `pizza place` → `pzza place` — **Acceptable** | `hotel` → `hostel` — **Bad** | A typo that lands on a real distinct word is not a typo |
| `auto repair` → `car repair` — **Good** | `attorney` → `lawyer` — **Acceptable** | Direct equivalence vs colloquial overlap across distinct categories |
| `starbucks` → `starbucks nyc` — **Good** | `starbucks` → `coffee shop` — **Bad** | Adding geo keeps the brand; generalizing drops it |
| `dentist` → `emergency dentist` — **Good** | `dentist` → `dental school` — **Bad** | Added attribute vs changed intent |
| `luxury hotel` → `5 star hotel` — **Acceptable** | `lux hotels` → `luxury hotel` — **Good** | See `resolved-tensions.md` |
