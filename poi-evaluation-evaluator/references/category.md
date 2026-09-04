# Category (§9)

Two questions at once: does the listed category describe the POI's **dominant
identity**, and is it the **best fit available** in the reference list?

| Option | Meaning |
|---|---|
| **Correct** | Accurately describes the dominant identity, and no other category is more relevant |
| **Approximate** | Accurately represents the POI, but is **overly broad** or only a partial fit — the list holds something more relevant |
| **Missing** | No category provided, but the reference list has one that fits |
| **Incorrect** | The category is not relevant to the POI |

## `Approximate` is the band Maps does not have

> An accurate-but-too-broad category is **`Approximate`, not `Correct`.**

This is the divergence that produced a wrong answer on a live assessment, where I
argued the option was a distractor because Maps has no such label. `Correct` requires
both accuracy *and* best fit. If a more specific, more relevant category exists in the
reference list, accuracy alone gets you `Approximate`.

Which means **rule 5 below is not optional**: check the reference list even when the
listed category looks fine, because `Correct` is a claim about the whole list, not
just about the listed string.

## The six rating rules (§9.1.2)

1. **Prioritise official sources.** A restaurant advertising steak and pizza but
   primarily serving steak is `dining ➡ restaurant ➡ steakhouse`.
2. **Then user reviews**, where official sources are absent or unreliable.
3. **On conflict, the official website wins** — over social media, and over reviews.
4. **If still unclear, use the POI name.** The **first** category keyword in the name
   is the best fit: `Orlando Pizza & Steakhouse` → `pizza_restaurant`.
5. **Always review the Category Reference List**, even when the listed category looks
   right, to confirm no better match exists.
6. **Never rely on categories assigned by other sources.** SERPs, maps services and
   review sites assign their own, and they do not follow these rules or this taxonomy.

## Anatomy of a category string (§9.1.3)

Levels run general → specific, separated by `➡`, with the **listed** category in bold
in the interface. The top level is L0.

```
dining ➡ restaurant ➡ latin american cuisine ➡ mexican cuisine ➡ taco restaurant
dining ➡ restaurant ➡ asian cuisine ➡ japanese cuisine ➡ donburi restaurant ➡ gyudon restaurant
```

The listed category can sit at any depth — L4 in the first, L5 in the second. Depth is
not itself a quality signal; fit is.

**No `Can't Verify` exists on Category.** Local knowledge is an approved input for
determining dominant identity.
