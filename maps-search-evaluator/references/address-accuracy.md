# Address Accuracy

Address accuracy evaluates how correctly each address component is displayed for a result. This rating is independent of relevance and name accuracy.

## Contents

- [Rating Scale](#rating-scale)
- [Address Components](#address-components)
- [Address Does Not Exist](#address-does-not-exist)
- [Correct with Formatting Issue](#correct-with-formatting-issue)
- [Language/Script Issue in Address](#languagescript-issue-in-address)
- [Can't Verify](#cant-verify)
- [Result Type Expectations](#result-type-expectations)

---

## Rating Scale

| Rating | When to Use |
|--------|------------|
| **Correct** | All address components are present, accurate, and in the expected format. Minor formatting differences that don't affect understanding are OK. |
| **Correct with Formatting Issue** | Address information is correct but has formatting problems (unexpected component order, redundant components, extra spacing, double commas). **Not** for misspellings — those are component-specific Incorrect ratings. |
| **Incorrect — [Component]** | One or more components are wrong or missing. Select the specific component checkbox(es). |
| **Address Does Not Exist** | The address does not exist in the real world (no building, no officially assigned plot of land). Use for address-type results only, NOT for POI addresses. |
| **Language/Script Issue** | Address details (not the title) are in an unexpected language or script. Expected languages: test locale, query language, result region language. |
| **Country-Specific Issue** | An address problem specific to the country's format that isn't covered by other checkboxes (e.g., missing municipality when required). |
| **Other Issue** | Issues not covered above: duplicate components, POI name in address details, natural features with street addresses, P.O. Box addresses. |
| **Can't Verify** | Cannot confirm as Correct or Incorrect due to lack of resources or unexpected address format on official sources. |

**Important rule**: Never select a component-specific checkbox AND a pattern-level issue checkbox for the **same problem**. For example, don't mark both "Language/Script Issue" and "Street Name" for the same language error. But you CAN mark a language issue AND an unrelated street number error.

---

## Address Components

Address components in order: **Street Number → Unit/Apt → Street Name → Sub-Locality → Locality → Region/State → Postal Code → Country**

### Street Number

| Scenario | Rating |
|----------|--------|
| Street number is wrong | Incorrect — Street Number |
| Street number is missing when the official address has one | Incorrect — Street Number |
| Street number extension missing (in markets that use them, e.g., Norway: "8c" vs "8") | Incorrect — Street Number (extensions are part of the street number, not unit numbers) |
| Street number extension incorrect (e.g., "4A" instead of "4B") | Incorrect — Street Number |
| Result number falls within official address range (e.g., "39" within "39-41") | ✅ Correct |
| Result number outside official range or wrong odd/even side | Incorrect — Street Number |
| Random/fake address range that doesn't exist | Incorrect — Street Number |

### Unit/Apt

| Scenario | Rating |
|----------|--------|
| Correct unit number matching official address | ✅ Correct |
| Unit number missing but required by official address | Incorrect — Unit/Apt |
| Wrong unit number | Incorrect — Unit/Apt |
| Unit number present but business doesn't list one and it can't be confirmed | Incorrect — Unit/Apt |

### Street Name

| Scenario | Rating |
|----------|--------|
| Correct street name | ✅ Correct |
| Wrong street name | Incorrect — Street Name |
| Missing street name | Incorrect — Street Name |
| Misspelled street name (including missing diacritics per country rules) | Incorrect — Street Name |
| Wrong street direction (missing "E" in "E El Camino Real") | Incorrect — Street Name |
| Extra street direction that doesn't exist ("E El Camino Real" when official is "El Camino Real") | Incorrect — Street Name |
| Wrong street type ("kade" instead of "plein") | Incorrect — Street Name |
| Valid alternate street name still in use | ✅ Correct |
| Former street name no longer in use | Incorrect — Street Name |

### Sub-Locality

| Scenario | Rating |
|----------|--------|
| Wrong sub-locality | Incorrect — Sub-Locality |
| Required sub-locality missing | Incorrect — Sub-Locality |

### Locality

| Scenario | Rating |
|----------|--------|
| Correct locality | ✅ Correct |
| Wrong locality | Incorrect — Locality |
| Missing locality | Incorrect — Locality |
| Misspelled locality (including missing diacritics per country rules) | Incorrect — Locality |
| Alternate accepted locality name | ✅ Correct |

### Region/State

| Scenario | Rating |
|----------|--------|
| Correct state/region | ✅ Correct |
| Missing state when mandatory (e.g., missing "CA" in USA) | Incorrect — Region/State |
| Wrong state/region | Incorrect — Region/State |
| Redundant but correct region in a market where it's not required | Correct with Formatting Issue |
| Redundant and wrong region | Incorrect — Region/State |

### Postal Code

| Scenario | Rating |
|----------|--------|
| Correct postal code | ✅ Correct |
| Wrong postal code | Incorrect — Postal Code |
| Missing postal code when mandatory | Incorrect — Postal Code |
| Non-mandatory postal code present and correct for at least part of the feature | ✅ Correct |
| US postal code with/without 4-digit extension | Ignore the extension; rate based on the 5-digit code |
| Multiple valid postal codes exist for a locality — any one is acceptable | ✅ Correct |

### Country

| Scenario | Rating |
|----------|--------|
| Result is in the same country as the test locale — country present or absent | ✅ Either is fine |
| Result is in a **different country** than the test locale — country present and correct | ✅ Correct |
| Result is in a **different country** than the test locale — country **missing** | Incorrect — Country |
| Country wrong | Incorrect — Country |

---

## Address Does Not Exist

Use **Incorrect — Address Does Not Exist** when:
- Strong evidence shows no building exists at the address AND no plot of land is officially assigned that address.
- In markets with street number extensions, the result shows a generic street number (e.g., "163 Main St") but only extension addresses exist (e.g., "163A" and "163B").
- An existing street address appears in a different locality than where it actually exists.

**Rules**:
- This rating applies only to **address-type results**, not to POI addresses.
- If you can't make an informed decision, rate **Can't Verify**.
- Leave a detailed comment with links.

---

## Correct with Formatting Issue

Use when all information is correct but not in the expected format:
- Components in unexpected order
- Non-required but correct additional components
- Extra spacing
- Double commas `[,,]`
- Valid but redundant or unnecessary components

**Do NOT use** for misspellings — those are component-specific Incorrect ratings.
**If a required component is missing**, rate Incorrect, not Correct with Formatting Issue.

---

## Language/Script Issue in Address

The address details must match the language/script of the test locale, query, or result region. Use this checkbox for language/script issues in address **details** (not the title — title issues use the result-level checkbox).

Exception: Added special characters not used in the expected language are not considered a language/script issue.

---

## Can't Verify

Use when the address cannot be confirmed as Correct or Incorrect:
- No official webpage found
- No official address listed
- Lack of official resources or street imagery
- Official source uses an unexpected format (intersection, exit, descriptive address)

**Key test**: Is the location given by the result address at least not wrong given all the information you've found?

### Can't Verify for Street Number
The street number must fall within the possible range of addresses for the street. If confirmed addresses nearby range from 103 to 175 and the result shows 165, it's within range → **Can't Verify**.

### Can't Verify for Street Name
If the official address uses a different format (e.g., intersection) but the result street provides access to the POI and the number is in range → **Can't Verify**.

---

## Result Type Expectations

### Business/POI Results

**Expected components**: Street number, street name, locality, region, postal code, country.

**Research sources** (in order of reliability):
1. Official website / chain store locator
2. Social media claimed by the business (updated within last 6 months)
3. Street imagery
4. Postal authorities
5. Government property registries
6. Primary publications, crowdsourced review sites

**Multiple official addresses**: If a business has more than one official address for the same physical location, accept any of them as Correct.

**Official source has obvious error**: If the official source misspells a city name and the result has the same error, rate the erroneous component **Incorrect** anyway.

### Alternative Official Addresses

#### Department Addresses
When a large entity (mall, university) has no complete street address on its official webpage:
- Result matches address of any department/entity at the same complex → ✅ **Correct**
- Result lists correct locality for the entity → ✅ **Correct**
- Locality is always expected even without a full address. If missing → **Incorrect — Locality**
- Adding the larger complex/campus name to the address → ✅ **Correct**

**But**: If the entity HAS its own official address and the result shows a DIFFERENT entity's address at the same complex → **Incorrect**.

#### Result Missing Street Address
- Both result and official website show identical incomplete addresses + correct locality → ✅ **Correct**
- Official website has street address but result is missing it → **Incorrect**

#### P.O. Boxes, Mailing Addresses, Management Offices
Addresses pointing to a different location (P.O. boxes, management offices, shared office spaces) → **Incorrect — Other Issue**.

#### Moving Entities
- Random location (unpredictable) → Rate "closed/does not exist"
- Fixed schedule (food trucks with posted schedule) → Correct address = longest stay location. Other addresses → Incorrect — Other Issue
- Fixed location (stationary vehicle) → Rate like standard business

### Address Type Results

| Result Type | Mandatory Components |
|-------------|---------------------|
| **Full address** | Street number, street name, locality, state, postal code (country if outside test locale) |
| **Street** | Street name, locality (for local roads). Highways don't require locality/state but if present, must be correct. |
| **Locality** | Locality, state (varies by country) |
| **Postal code** | Postal code, locality, state |
| **State/Region** | State/region name (+ country if user is in a different country) |
| **Country** | Country name only |

### Features Without an Expected Address

These POIs do not require a street address. Includes: parks, monuments, landmarks, heritage sites, bridges, squares, parking lots, transit POIs (airports, ferry ports, subways, bike stations, train/bus stops).

#### Minimum Component
- **Locality** is required when the POI fits entirely within one locality.
- POIs spanning multiple localities do NOT require a locality.

#### Natural Features (rivers, mountains, ecosystems)
- Should NOT have street addresses. If one is returned → **Incorrect — Other Issue** (even if it points to an associated building like a ranger station).
- Locality is acceptable if appropriate for the feature's size (small hot spring → OK; large mountain → not OK → Incorrect — Other Issue).
- State is acceptable.
- If a natural feature spans multiple countries, any one country is Correct. No country at all is also Correct.
- Parks protecting natural features (named after them) can have the official park address.

#### Official Address Present
When a POI without expected address has an official street address:
- Full address matching official → ✅ **Correct**
- Street-only matching official street → ✅ **Correct**
- Full address with wrong street number → **Incorrect — Street Number**
- Different street name → **Incorrect — Street Name**
- No address at all (missing locality) → **Incorrect — Locality**

#### Official Address is Partial
When official address is a partial street (no number):
- Result has full address, street matches, number doesn't belong to another POI → **Can't Verify**
- Result has full address, number belongs to another building → **Incorrect**

#### No Official Address
- Result has full address, building is associated with POI, street provides access → **Can't Verify**
- Result has full address, belongs to another unrelated building → **Incorrect**
- Result has street only, street provides access to POI → **Can't Verify**

**"Provides access"** means a person can reach the POI directly from the given street by walking or driving. Includes:
- Streets following the feature's boundary or leading into it
- T-intersections (street continues on the other side)
- Does NOT include: streets ending at a T-intersection where the feature is on the other side and the street doesn't continue
- Ignore access restrictions
