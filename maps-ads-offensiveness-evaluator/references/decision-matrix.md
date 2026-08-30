# The Decision Matrix

Use with `../SKILL.md`. This file turns the guideline into a lookup. Work it in three steps and the rating falls out. Do not skip to a verdict.

Offensiveness on this task is not a property of the ad. A liquor store ad is offensive next to `alcohol addiction treatment center` and perfectly fine next to `Starbucks`. It is the **pair** that is rated, so both sides must be classified before anything is decided.

## Contents

- [Step 1: classify the query](#step-1-classify-the-query)
- [Step 2: classify the ad](#step-2-classify-the-ad)
- [Step 3: cross them](#step-3-cross-them)
- [The override rules](#the-override-rules)
- [Cells the guideline does not decide](#cells-the-guideline-does-not-decide)

## Step 1: classify the query

Read the query and put it in exactly one class. If two seem to fit, take the one higher in this list.

| Class | The query is | Examples |
|---|---|---|
| **A. Kids and family** | for a child- or family-focused place, or a place whose primary audience is children even when no child word appears | `preschool`, `kids birthday party venue`, `school`, `Legoland`, `Great Wolf Lodge` |
| **B. Religious** | for a place of worship, a religious institution, or religiously observant food | `mosque`, `church`, `synagogue`, `temple`, `halal food`, `kosher` |
| **C. Medical, health and recovery** | for care or treatment of **a person**: the user, or someone they are caring for. A health condition, pregnancy, or recovery from addiction | `urgent care`, `hospital`, `prenatal`, `cancer treatment center`, `oncology`, `sexual health clinic`, `alcohol addiction treatment center` |
| **D. Safety-critical** | for something the user is about to drive, operate, or be transported by | `car rental near me`, `gas station`, `driving school` |
| **E. Grief and death** | for a place tied to death, burial or mourning | `cemetery`, `funeral home`, `crematorium` |
| **F. Values-committed** | for a place chosen out of a stated ethical or dietary commitment | `vegetarian restaurants`, `vegan`, `animal shelter` |
| **G. Already adult or sensitive** | itself for an adult or sensitive venue | `bar near me`, `casino`, `liquor store`, `strip club` |
| **H. Generic** | anything else. Most queries land here | `hotel`, `McDonald's`, `Starbucks`, `veterinary hospital`, `hardware store` |

**Misspellings.** Rate the intent, not the letters. `preschoool` is class A, because the user is very likely looking for a preschool. Take the best guess and say in the comment what you took it to be.

**Foreign language.** Translate first, then classify. Never classify from the script alone.

**Cannot tell what the place is.** Open the Maps link or the website. Class H is the default only after you have looked, never because you did not.

**Animal care is not class C.** A `veterinary hospital`, a vet clinic or a pet hospital is class H, because the vulnerability the medical scenario protects is a person's own health. The guideline rates `veterinary hospital` against a paint store ad as Not Offensive and treats it as an ordinary query. Class C is for human care.

## Step 2: classify the ad

Read the advertised POI and put it in one hazard class. Judge the business, not its name.

| Hazard | The ad is for | Examples |
|---|---|---|
| **1. Alcohol** | anywhere whose business is alcohol | bar, pub, brewery, winery, wine bar, liquor store, `Total Wine & More`, `The Tap Room`, `Voodoo Brewing Co.` |
| **2. Gambling** | a casino or betting venue | `Empire City Casino`, `Cherokee Casino` |
| **3. Adult entertainment** | an adult venue or adult content | nightclub billed as adult entertainment, strip club |
| **4. Tobacco and vape** | smoke shop, vape shop, cigar lounge | |
| **5. Meat-specific** | a butcher or meat market. **A restaurant is never in this class**, whatever it serves | `3 Arrows Boutique Butcher` |
| **6. Hunting and firearms** | hunting outfitter, gun shop, shooting range | `Backwoods Hunting Outfitters` |
| **7. Funeral and end-of-life** | funeral home, cemetery, cremation, hospice marketing | `Restland Funeral Home` |
| **8. Adult-themed body services** | plastic surgery, tattoo parlour | |
| **9. Benign** | anything else. Most ads land here | grocery store, paint store, hotel, restaurant, `Burger King` |

## Step 3: cross them

Find the query class down the side and the ad hazard across the top.

| | 1 Alcohol | 2 Gambling | 3 Adult ent. | 4 Tobacco | 5 Meat | 6 Hunting | 7 Funeral | 8 Surgery/tattoo | 9 Benign |
|---|---|---|---|---|---|---|---|---|---|
| **A Kids/family** | **Majority** | **Majority** | **Majority** | **Majority** | Not Off. | judgement | judgement | **Majority** | **Not Offensive** |
| **B Religious** | **Majority** | **Majority** | **Majority** | **Majority** | Majority *(dietary religions only)* | judgement | Not Off. | judgement | **Not Offensive** |
| **C Medical/recovery** | **Majority** | **Majority** | **Majority** | **Majority** | Not Off. | judgement | **Majority** | judgement | **Not Offensive** |
| **D Safety-critical** | **Majority** | Not Off. | Not Off. | Not Off. | Not Off. | Not Off. | Not Off. | Not Off. | **Not Offensive** |
| **E Grief/death** | Some | **Some** | Some | Not Off. | Not Off. | judgement | Not Off. | Not Off. | **Not Offensive** |
| **F Values-committed** | Not Off. | Not Off. | Not Off. | Not Off. | **Some** | **Some** | Not Off. | Not Off. | **Not Offensive** |
| **G Already adult** | **Not Offensive** | **Not Offensive** | **Not Offensive** | Not Off. | Not Off. | Not Off. | Not Off. | Not Off. | **Not Offensive** |
| **H Generic** | **Not Offensive** | **Not Offensive** | Not Off. | Not Off. | Not Off. | Not Off. | Not Off. | Not Off. | **Not Offensive** |

Cells in bold are decided by the guideline text or by one of its worked examples. Cells marked *judgement* are not covered; see the last section.

Read the bottom two rows carefully, because they are where over-rating happens. `Starbucks` → a bar is **Not Offensive**. `Hotel` → a resort with a casino is **Not Offensive**. `bar near me` → another bar is **Not Offensive**. An adult-category ad against a generic query is not offensive by itself.

Read the last column carefully too, because it is where the relevance instinct leaks in. A benign ad is **Not Offensive** against every query class, however unrelated. `veterinary hospital` → a paint store is Not Offensive. `hospital` → a grocery store is Not Offensive.

## The override rules

Apply these after the matrix. Each one beats the cell it lands on.

1. **Recovery query, ad promotes the substance.** If the query is about recovery from an addiction and the ad promotes that substance or activity, it is **Majority**. This is stated in the guideline and it covers gambling recovery as well as alcohol and drugs.
2. **Religion mismatch is never offensive.** A mosque ad on a `church` query, or any other cross-religion pairing, is **Not Offensive**. Only a violation of the queried religion's own prohibitions counts.
3. **Restaurants and cuisine are never the meat hazard.** For a vegetarian, vegan or religiously observant query, a restaurant of any cuisine is **Not Offensive**, because any restaurant can serve suitable food. Only a butcher or meat market triggers hazard 5. The guideline states this twice, once for values queries and once for religious ones.
4. **Ambiguous query, sensitive reading surfaced.** If the ad appears to have matched a sensitive *word* in the query rather than the user's actual meaning, rate the alarm it causes rather than the matrix cell. `death valley` (a national park) → a funeral home. `target range` (a shooting range) → a Target retail store. Default to **Some**, and go to **Majority** where the surfaced reading is death, illness or violence.
5. **Competitors are never offensive.** Two businesses in the same category is a relevance observation, not an offensiveness one. `McDonald's` → Burger King is **Not Offensive**.

## Cells the guideline does not decide

Six cells above are marked *judgement*. The guideline says explicitly not to limit yourself to its scenarios, so these are yours to decide. Decide them with the test in `majority-vs-some.md`, and say in your output that the pair was not covered by a named scenario.

Do not silently invent a rule and present it as the guideline. Do not refuse to rate either. Take the judgement, name it as judgement, and explain the harm you think the user would feel.
