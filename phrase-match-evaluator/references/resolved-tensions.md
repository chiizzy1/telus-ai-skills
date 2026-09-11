# Resolved Tensions

The Phrase Match guideline states two rules that its own examples contradict. Both are load-bearing — they decide common pairs — so each needs a settled operative reading rather than a choice made fresh each time. That is what this file fixes.

Neither resolution overrides the guideline. Each one reconciles a general statement with the specific examples the same document gives, on the principle that a worked example is a decided case and a summary sentence is a summary.

## 1. The substring baseline is a floor, not a verdict

**What page 2 says:**

> Baseline: If the keyword appears as a complete substring in the query, it's automatically considered good. This is the simplest, most reliable matching rule. When you see the exact keyword text within the query, rate it good.

**What the same document's examples say:**

| Pair | Substring present? | Guideline rating |
|---|---|---|
| `church` → `churchs chicken` | yes | **Acceptable** |
| `apple` → `apple bee` | yes | **Acceptable** |
| `beach` → `palm beach outlets` | yes | **Acceptable** |
| `apple` → `caramel apple` | yes | **Acceptable** |
| `apple` → `applebees` | as characters, yes | **Bad** |

Four Acceptables and a Bad, all of them substring matches. Taken literally the baseline would overturn all five.

**Operative rule.** Two corrections, in order:

1. **Substring means token, not characters.** The keyword must survive in the query as a whole word — inflection, plural and possessive still count (`church` → `church**s** chicken` qualifies). A keyword buried inside an unrelated longer word does not. This is what the Bad #17 note means by *"Loses the phrase 'apple' from being included in the query."*
2. **Token containment sets a floor of Acceptable, and earns Good only when the sense survives.** If the query rebinds the keyword's token to a different entity — a brand absorbing a common word — the rating is Acceptable, because the advertiser may be surprised even though the intent is technically contained.

So: `walmart` → `walmart supercenter` is Good because the sense is unchanged. `church` → `churchs chicken` is Acceptable because a religious-intent advertiser has been matched to fried chicken.

**Why this reading and not the other.** The baseline sentence is written as a convenience heuristic for the easy majority ("the simplest, most reliable matching rule"), and the document immediately follows it with *"Substring matching catches the obvious cases, but users don't always use exact terms."* The Acceptable band exists specifically for contained-but-surprising matches; reading the baseline literally would empty that band of four of its thirteen listed examples.

**Practical consequence.** A naive agent rating from page 2 alone will call `church` → `churchs chicken` Good. That is wrong, and it is the single most predictable error on this rubric.

## 2. The head/variant asymmetry is about brands

**What pages 5–6 say:**

> Head Form keywords match to their variants: `McDonald's` → `McD` ✅
> Variant keywords don't match to head form: `McD` → `McDonald's` ❌
> Bad — Asymmetric Alternate Spelling Matching: `starbux` → `starbucks` (alternate spelling should not match legitimate brand name)

**What page 2 says:**

> Semantic Equivalents — Good: `lux hotels` → `luxury hotel` (abbreviation to full form)

`lux` is an abbreviation and `luxury` is the full form, so this is variant → head. Under the pages 5–6 rule it would be Bad. It is listed as Good.

**Operative rule.** The head/variant asymmetry governs **brand names only**. Every example the guideline uses to define it is a brand: McDonald's, Starbucks, Best Buy, Raising Cane's. Generic descriptors are not brands and are not subject to it — an abbreviation of a common adjective expanding to its full form is an ordinary semantic equivalent, and Good.

**Why the asymmetry exists for brands at all.** A brand abbreviation is ambiguous in a way a generic abbreviation is not. `mcd` could be McDonald's, MCD Auto Services, or an initialism for something else, so an advertiser who bought `mcd` should not be matched to the unambiguous `mcdonalds` — they may not have meant that brand. `lux` expanding to `luxury` carries no such risk, because neither string names an entity.

**Practical consequence.** Before applying Step 6 of the decision procedure, ask whether the shortened string names a *brand*. If it names a quality, category or attribute, use Step 5 instead.

**Confidence, stated honestly.** This is the weaker of the two resolutions. The alternative reading — that the `lux hotels` example is simply an error in a July 2026 document with several visible typos (`cender`, `susprised`, `hote`) — is plausible. The brand/generic split is the reading that keeps both passages true, so it is what this skill applies, but **flag any live pair that turns on it** rather than rating silently. A pair like `econ car rental` → `economy car rental` sits exactly on this line.

## How to handle a pair that turns on either tension

Rate it under the operative rule above, then say so in one line:

> Rated Acceptable rather than Good: the keyword's token is present but the query rebinds it to a different brand. The guideline's substring baseline reads as automatic Good, but its own `church` → `churchs chicken` and `apple` → `apple bee` examples are Acceptable on the same pattern.

That gives the reviewer the rating and the reason to overrule it, which is the right division of labour when a source document disagrees with itself.
