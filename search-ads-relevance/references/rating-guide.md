# Search Ads Relevance Rating Guide

Use this reference before rating a live TELUS Search Ads Relevance task. The main `SKILL.md` contains the workflow and compact rules; this file contains the detailed decision framework, examples, and game-specific evaluation criteria.

## App Query Decision Framework

Rate based on how the ad relates to the user intent conveyed by the query, considering **functionality** and **target audience**.

### Excellent (Apps)

The ad directly satisfies the user's intent. Apply when:

- **Exact match**: The ad IS the app the user searched for.
- **Direct competitor**: Apps competing for the same users with the same core functionality (Uber↔Lyft, WhatsApp↔Messenger, Netflix↔Hulu).
- **Developer name query**: The ad is from that developer (query "adobe" → ad "Adobe Lightroom" → Excellent).
- **Broad category query**: The ad clearly fits (query "fitness" → any legitimate fitness app → Excellent).

### Good (Apps)

The ad is logically linked and quite likely to interest the user, but the connection is weaker:

- **Related but different functionality**: Query "doordash" → ad "Pizza Hut Delivery" (food delivery, but limited scope).
- **Accessory/add-on apps**: Query "youtube" → ad "Video Tube™ stream player" (complements the queried app).
- **Overlapping but not identical features**: Query "english spanish dictionary" → ad "Camera Translator" (related translation intent).
- **Same developer, different theme**: Query "disney emoji blitz" → ad "Star Wars Puzzle Droids" by Disney (same developer, similar mechanics, different theme).

### Acceptable (Apps)

The link is weak but recognizable — user wouldn't be surprised or offended, but probably isn't interested:

- **Vague category overlap**: Query "photo collage" → ad "Flyer Maker" (both graphic design, different purpose).
- **Broad financial overlap**: Query "american express" → ad "Coinbase" (both finance, very different niches).
- **Tangential educational link**: Query "khan academy" → ad "Elevate Brain Training" (vaguely related to learning).
- **App relevant but NOT available in test locale** → Acceptable (hard rule).
- **Same developer, no thematic match** → At least Acceptable (floor rule).

### Bad (Apps)

No perceivable link, or the link is illogical/offensive. MUST leave a comment.

| Pattern | Example | Why Bad |
|---|---|---|
| No perceivable link | Banking app → Birdwatching ad | Completely unrelated |
| Same word, different context | Document scanner → Virus scanner | "Scanner" used differently |
| Technically linked but illogical | Grocery shopping → Clothes shopping | Different audiences entirely |
| Same broad category, different niches | Dog training → Cat training | No basis to assume cross-interest |
| Algorithm misspelling | "lego" → "letgo" | Not what the user searched for |
| Offensive mismatch | "serene noises" → Gun database | Potentially upsetting |
| Age/audience mismatch | "multiplication for kids 2nd grade" → Kindergarten math | Wrong age group, too specific to stretch |

## Game Query Decision Framework

Games are rated differently from apps. Users looking for games want **entertainment**, not functionality. Evaluate on THREE axes:

| Axis | What to Compare |
|---|---|
| **Play style** | Reflexes vs strategy vs puzzle vs idle vs simulation |
| **Presentation** | Realistic vs cartoony vs dark/horror vs colorful |
| **Audience** | Children vs casual vs hardcore vs sports fans |

### Excellent (Games)

The ad game shares enough play style AND themes to appeal to the same users:

- Query "racing games" → any racing game → Excellent.
- Query "pubg" → "Rules of Survival" (same Battle Royale genre) → Excellent.
- Query "clicker heroes" → "Idle Heroes" (both idle RPGs with fantasy theme) → Excellent.

### Good (Games)

Close enough to be logical and potentially interesting, but weaker link:

- Query "strategy game" → "Idle Heroes" (some strategic elements, but more RPG) → Good.
- Query "spiral roll" → "Pencil Marking" (different theme, same hand-eye coordination mechanic) → Good.
- **Game accessory apps**: Query "minecraft" → "Addons for Minecraft" → Good.

### Acceptable (Games)

User understands why they see it, but probably won't click:

- Query "fun run" (cartoon running game) → "Nitro Nation" (realistic car racing) → Acceptable (both racing-adjacent, very different style).
- Query "call of duty" (realistic war shooter) → "Drogon War" (fantasy dragon shooter) → Acceptable.
- Query specifies "new" but ad app is old/outdated → downgrade accordingly.

### Bad (Games)

Completely and/or jarringly different from user intent:

- Puzzle (slow thought) vs Action (quick reactions).
- WW2 realistic combat vs Cartoon farm building.
- Cute puppy game vs Dark fantasy RPG ("puppydog clicker" → "Idle Heroes").
- Street basketball vs Gymnastics ("dunknation 3x3" → "Gymnastics Superstar").
- Zombie horror driving vs Children's puzzle ("zombie highway" → "Kids Puzzles Puzzingo").

## Intent Range Quick Reference

```
Query "gym app":
  Gym workout tracker          → Excellent (direct match)
  Running/jogging tracker      → Good (broader fitness interest)
  Nutrition tracker            → Acceptable (tangentially related to gym-goers)
  Birdwatching app             → Bad (no connection)
```

## Comment Examples

> The query is for Uber Eats, a food delivery service. This ad is an exact match for the queried app, making it directly relevant to the user's intent. Rated Excellent.

> The user is looking for DoorDash, a general food delivery app. Pizza Hut's delivery app covers a similar use case but is limited to one restaurant chain, so it's quite likely to interest the user while not being an ideal match. Rated Good.

> The query is for Khan Academy, an online learning platform. Elevate's brain training games are vaguely related to learning but serve a very different purpose, so the user wouldn't be surprised to see this ad but probably isn't interested. Rated Acceptable.

> The query is for a serene noises app, suggesting the user wants calming audio content. A gun firearm database has no connection to this intent and could be offensive given the user's interest in relaxation. Rated Bad.

> The query intent is likely the Arno test prep app. iHuman Chinese is a children's app for learning Chinese characters, which has no overlap with the query intent.

**Conciseness rule:** State the intent, state the connection (or lack of it), stop. Do not over-explain or list what the ad app does in detail. The comment above is the ideal length and style.

## Decision Checklist

Run through before finalizing every rating:

- [ ] Did I research the query to understand user intent?
- [ ] Did I research the advertised app's actual functionality?
- [ ] Am I rating based on INTENT, not keyword overlap?
- [ ] Did I consider the full range of interests the query implies?
- [ ] Did I check if this is a same-developer situation? (floor = Acceptable)
- [ ] Did I check if this is a direct competitor? (= Excellent)
- [ ] Did I check if this is an accessory app? (= Good)
- [ ] Is the app available in the test locale? (if not, cap = Acceptable)
- [ ] Am I wrongly demoting for price, reviews, or description quality?
- [ ] For game queries: did I evaluate play style, presentation, AND audience?
- [ ] Does the query specify "new" or "popular"? Did I check app freshness?
- [ ] Did I consider locale-specific meaning of the query?
- [ ] If rating Bad, did I write a mandatory comment explaining why?
- [ ] Does my comment follow the style rules (concise, human, no AI filler)?
