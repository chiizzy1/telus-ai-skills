# Name and Category Accuracy

This rating evaluates the accuracy of both the Business/POI **name** and its **category** together. The final rating reflects the combined accuracy of both elements.

## Contents

- [Rating Scale](#rating-scale)
- [Name Evaluation](#name-evaluation)
- [Category Evaluation](#category-evaluation)
- [Summary Table: Final Name & Category Accuracy Rating](#summary-table-final-name-category-accuracy-rating)
- [Transit Names](#transit-names)
- [Parking Names](#parking-names)

---

## Rating Scale

| Rating | When to Use |
|--------|------------|
| **n/a** | All **address-type results** (residential addresses, streets, localities, postal codes, states, countries). These have no name or category to rate — the first line of the address appears as the title. |
| **Correct** | Name matches official sources AND category is correct (or missing/listed as N/A). |
| **Partially Correct** | Name is recognizable but has minor issues AND category is correct (or missing). |
| **Incorrect** | Name is unrecognizable OR category is wrong. **An incorrect category always makes the final rating Incorrect**, regardless of name accuracy. |
| **Can't Verify** | Name cannot be confirmed or denied with available resources, and nothing is objectively wrong. |

**Demotion checkboxes** (for Partially Correct or Incorrect): Select **Name Issue**, **Category Issue**, or both.

---

## Name Evaluation

### Step 1: Determine the Official Name

Research the official name using these sources (in order of reliability):

**Primary sources:**
- Chain business locator page on the official website
- About/About Us section on the entity's official website
- Signs and storefronts seen on official sites or social media pages
- Claimed social media pages

**Secondary sources** (when primary sources are unavailable):
- Signs and storefronts seen on recent street/online imagery or crowdsourced review pages
- Recent articles in primary publications (newspapers doing their own reporting)
- Official restaurant menus (user photos or scanned images)

**If the name cannot be confirmed** with these resources and nothing is objectively wrong → **Can't Verify**.

### Step 2: Rate the Name

#### Correct Name ✅

A name is correct when it is used on the POI's official website or other official resources. Even if the official website doesn't use the name, if other official sources do, the name is correct. **The name must refer to the particular POI** — a corporate name alone is not automatically the correct name for a specific location.

**Correct name scenarios:**

| Scenario | Example | Rating |
|----------|---------|--------|
| **Exact match** | Result: "McDonald's", Official: "McDonald's" | ✅ Correct |
| **Storefront name** | Result: "Peet's Coffee", Official: "Peet's – Polk Street" (name on storefront) | ✅ Correct |
| **Corporate brand on signage** | Result: "Best Buy", Official: "Best Buy San Jose" (but sign shows just "Best Buy") | ✅ Correct |
| **Microsoft stores** | Result: "Microsoft", Official: "Microsoft Store" (storefront shows only logo) | ✅ Correct |
| **Location modifier present but missing** | Result: "Apple", Official: "Apple Valley Fair" (modifier missing but store is identifiable) | ✅ Correct |
| **Location modifier added** | Result: "Old Navy – Belle Isle Station", Official: "Old Navy" (modifier not official but correct) | ✅ Correct |
| **Affiliation added** | Result: "Delgado Community College – Charity School of Nursing", Official: "Charity School of Nursing" | ✅ Correct |
| **Stylized characters** | Result: "Toys 'R' Us", Official: "Toys Я Us" (special character in logo) | ✅ Correct |
| **"The" missing** | Result: "Home Depot", Official: "The Home Depot" (commonly referred to without "The") | ✅ Correct |

**Location modifier rules:**
- A modifier (city name, mall name, etc.) can be included even if not officially used, as long as it is correct. If the modifier is **misspelled**, the name becomes **Partially Correct**.
- A missing modifier is OK as long as the business is identifiable without it.
- Some modifiers are essential for differentiation (e.g., "University of California **Irvine**" — "Irvine" differentiates from other UC campuses). If the essential modifier is missing → **Partially Correct**.

**International/bilingual names:**
- Some official websites have local and international (English) versions. Only consider the English version if English is the language of the test locale, query, or result region, or if the English brand name is commonly used in the market.

#### Partially Correct Name ⚠️

A partially correct name differs from the official version but **can still be recognized by the user**.

**Partially correct scenarios:**

| Issue Type | Example | Rating |
|------------|---------|--------|
| **Missing punctuation** | Result: "Macys", Official: "Macy's" (missing apostrophe) | ⚠️ Partially Correct |
| **Missing special character** | Result: "HM", Official: "H&M" (missing ampersand) | ⚠️ Partially Correct |
| **Duplicated name** | Result: "uhaul uhaul", Official: "U-Haul" | ⚠️ Partially Correct |
| **Unexpected form** | Result: "Seven Eleven", Official: "7-Eleven" | ⚠️ Partially Correct |
| **ALL CAPS** | Result: "GAMESTOP", Official: "GameStop" | ⚠️ Partially Correct (unless ALL CAPS is the business's style) |
| **Minor/moderate misspelling** | Result: "Mosjaw", Official: "Moosejaw" (2 missing letters, still identifiable) | ⚠️ Partially Correct |
| **Multiple minor issues** | Result: "Ecofuture Buildng Co", Official: "Ecofutures Building Inc" | ⚠️ Partially Correct |
| **Extra descriptive words** | Result: "Napoli Coffeehouse & Pastries", Official: "Napoli Coffee" (extra parts match the business) | ⚠️ Partially Correct |
| **Extra non-misleading word** | Result: "GAP Superstore", Official: "GAP" | ⚠️ Partially Correct |
| **Mix of expected languages** | Result: "BerkeleyLaw Univerzitní of California" (Czech locale, mix of English and Czech) | ⚠️ Partially Correct |
| **URL-based name** | Result: "att", Official: "AT&T" (URL lacks formatting) | ⚠️ Partially Correct |
| **Essential modifier missing** | Result: "University of California", Official: "University of California Irvine" | ⚠️ Partially Correct |
| **"The" added** | Result: "The Sears", Official: "Sears" (business never uses "The") | ⚠️ Partially Correct |
| **Corporate structure addendum** | Result: "IT'SUGAR LLC", Official: "IT'SUGAR" | ⚠️ Partially Correct |
| **Corporate structure** | Result: "Nordstrom, Inc.", Official: "Nordstrom" | ⚠️ Partially Correct |

**Service-level mismatch in name:**
When a chain name includes the wrong service level:
- Result: "Patagonia Outlet", Official: "Patagonia" (not an outlet) → ⚠️ **Partially Correct**
- Result: "Delhaize", Official: "Delhaize Supermarkt" (missing service indicator) → ⚠️ **Partially Correct**
- Result: "Best Buy", Official: "Best Buy Express" (vending machine vs. store) → ⚠️ **Partially Correct**

**Acronyms**: ALL CAPS is expected for acronyms (e.g., "YMCA", "TGIF").

#### Incorrect Name ❌

An incorrect name **cannot be recognized** because of severe misspelling, ambiguity, or fundamentally wrong information.

**Incorrect scenarios:**

| Issue Type | Example | Rating |
|------------|---------|--------|
| **Severe misspelling — meaning change** | Result: "Taco Bull", Official: "Taco Bell" (could be a different business) | ❌ Incorrect |
| **Short name, small error** | Result: "IEA", Official: "IKEA" (short names are very sensitive to errors) | ❌ Incorrect |
| **Severe misspelling — unidentifiable** | Result: "Zatas Tacos + Tequila", Official: "Zacatecas Tacos + Tequila" | ❌ Incorrect |
| **Holding company name** | Result: "JAB Holding Company", Official: "Peet's Coffee" (completely different) | ❌ Incorrect |
| **Ambiguous extra word** | Result: "Walgreens Pizza", Official: "Walgreens" (user can't tell if it's a pizzeria or pharmacy) | ❌ Incorrect |
| **Missing critical word** | Result: "Cheesecake", Official: "The Cheesecake Factory" (can't identify the chain) | ❌ Incorrect |
| **Similar but different company** | Result: "UPS", Official: "USPS" (entirely different companies) | ❌ Incorrect |
| **Swapped word** | Result: "Starbucks & Spencer", Official: "Marks & Spencer" | ❌ Incorrect |
| **Slang** | Result: "Mickey D's", Official: "McDonald's" (slang, not official) | ❌ Incorrect |
| **Former name** | Result: "Sommet Center", Official: "Bridgestone Arena" (former name no longer shown officially) | ❌ Incorrect |

**Key rule**: If the name is incorrect, the **final Name & Category Accuracy rating is always Incorrect**, even if the category is correct.

---

## Category Evaluation

The category appears below the address details. Not every result has a category — if missing or listed as N/A, do **not** demote.

### Correct Category ✅
The category accurately reflects the business, service, or function. Includes broad or alternate categorizations that are not misleading.
- "French Cuisine" for a French restaurant → ✅ Correct
- "Restaurant" for a French restaurant → ✅ Correct (slightly too general but not misleading)
- Categories can vary by market. Localization should be considered.

### Incorrect Category ❌
The category is wrong, misleading, misspelled, incomplete (missing parts or odd abbreviations), or in an unexpected language/script.

**When the category is incorrect, the final Name & Category Accuracy rating is ALWAYS Incorrect**, even if the result name is Correct or Partially Correct.

| Scenario | Example | Final Rating |
|----------|---------|-------------|
| Correct name + incorrect category | Result: "Jocko's World Famous" (steakhouse), Category: "Pizza Restaurant" | ❌ Incorrect |
| Partially correct name + incorrect category | Name has minor misspelling + wrong category | ❌ Incorrect |
| Correct name + misspelled category | Category has typos | ❌ Incorrect |
| Correct name + category in wrong language | Category in unexpected language/script | ❌ Incorrect |

---

## Summary Table: Final Name & Category Accuracy Rating

| Name Rating | Category Rating | Final Rating |
|-------------|----------------|-------------|
| Correct | Correct (or missing) | **Correct** |
| Correct | Incorrect | **Incorrect** |
| Partially Correct | Correct (or missing) | **Partially Correct** |
| Partially Correct | Incorrect | **Incorrect** |
| Incorrect | Correct (or missing) | **Incorrect** |
| Incorrect | Incorrect | **Incorrect** |
| Can't Verify | Correct (or missing) | **Can't Verify** |
| n/a (address result) | — | **n/a** |

---

## Transit Names

Transit POI names follow the same rules as business/POI names. Research the official name using transit authority websites, official maps, and signage.

## Parking Names

Parking lot and parking structure names follow the same rules. Research using official signage, maps, and business owner information.
