# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

A user types a plain-language query like "vintage graphic tee under $30, size M" and FitFindr searches 40 thrift listings for matches. If it finds any, it picks the best match and asks the model to suggest 2-3 outfits that pair the item with the user's saved wardrobe — or general styling advice if the wardrobe is empty. It then generates a short social-media caption (the fit card) for the outfit. If the search comes back empty, the agent stops early and tells the user specifically which filter to loosen (keywords, size, or price).

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings file for items matching a description, size, and price ceiling.
- **Inputs:** `description` (str), `size` (str), `max_price` (float)
- **Returns:** A list of listing dicts, each with id, title, description, category, style_tags, size, condition, price, colors, brand, platform.
- **When it has nothing:** Returns an empty list `[]`, never `None`.

### `suggest_outfit`

- **What it does:** Takes a thrifted item and the user's wardrobe and suggests outfits pairing them.
- **Inputs:** `new_item` (dict, one listing), `wardrobe` (list of wardrobe item dicts)
- **Returns:** A string of 2-3 outfit ideas.
- **When it has nothing:** If `wardrobe` is `[]`, returns a string of general styling advice for the item instead of failing.

### `create_fit_card`

- **What it does:** Writes a short caption someone would post about the outfit.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A string caption, 1-3 sentences.
- **When it has nothing:** If `outfit` is empty, returns an empty string `""`.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, set session["message"] to a message naming what to change (size, price, or keywords) and stop, leaving session["fit_card"] as None. Otherwise set session["selected_item"] to the first result and go to suggest_outfit, then create_fit_card.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex in `agent.py::_parse_query`. Price is extracted by matching patterns like "under $30" or "max $30". Size is extracted by matching "size XL" or bare tokens like S, M, L, XL. The remaining text becomes the description passed to `search_listings`.

**What moves through the session:** search results -> selected_item -> outfit -> fit_card

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are 3 outfit suggestions that pair the Y2K Butterfly Baby Tee with
            pieces from your current wardrobe:

            Outfit 1: Off-Duty Y2K Contrast — baby tee + dark wash baggy jeans +
            chunky white sneakers + black crossbody bag

            Outfit 2: Elevated Retro-Casual — baby tee + wide-leg khaki trousers +
            vintage black denim jacket + brown leather belt + combat boots

            Outfit 3: Layered Transitional Streetwear — baby tee + black cropped zip
            hoodie (open) + dark wash baggy jeans + chunky sneakers

  Fit card: Scored this Y2K butterfly baby tee on Depop for just $18 and I'm
            officially in my early 2000s street-style era. 🦋 Can't wait to style
            this with baggy denim and chunky sneaks, or layer it under a zip-up
            hoodie. Tell me which outfit combo is your favorite!
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', ...}, ...]

$ python -c "from tools import search_listings; print(search_listings('neon green snowsuit', max_price=5))"
[]
```

```
$ python -c "from tools import search_listings, suggest_outfit; item = search_listings('graphic tee', max_price=30)[0]; print(suggest_outfit(item, []))"
That Y2K butterfly baby tee is a super versatile find! Because it sits right at the intersection of Y2K nostalgia and soft cottagecore, you can take it in a few different directions depending on your vibe.

Since you don't have a saved wardrobe yet, here are 3 easy, staple-based outfit formulas you can build using basic pieces you can easily find thrifted or retail:

### 1. The Ultimate Y2K Mall-Rat Look
* Bottoms: Low-rise or mid-rise baggy cargo pants in a neutral (olive green, beige, or grey)
* Footwear: Chunky platform sneakers
* Accessories: Small nylon shoulder bag, rimless tinted sunglasses, butterfly claw clips

### 2. The Soft Cottagecore Picnic Vibe
* Bottoms: A white or cream tiered midi skirt or a denim button-front mini skirt
* Footwear: Strappy brown leather sandals or canvas slip-ons
* Accessories: Woven straw tote bag, dainty silver pendant necklace

### 3. The Off-Duty Model / Casual Streetwear
* Bottoms: Vintage-wash straight-leg or mom jeans
* Outerwear (optional): Oversized faux-leather racer jacket or flannel tied at the waist
* Footwear: Retro low-profile sneakers (Adidas Sambas, Gazelles, Nike Cortez)
```

```
$ python -c "from tools import search_listings, create_fit_card; item = search_listings('graphic tee', max_price=30)[0]; print(create_fit_card('Pair with dark jeans and boots', item))"
Still kicking myself for scoring this butterfly baby tee for just $18 on Depop. Honestly obsessed — just need to pair it with some dark wash jeans and chunky boots for the ultimate off-duty model look.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Claude to implement `suggest_outfit` to take `new_item` and `wardrobe` as arguments, handling an empty wardrobe by returning general advice.
- *What came back:* The implementation called `wardrobe.get("items", [])`, which assumed wardrobe was always a dict. When tested with `suggest_outfit(item, [])` — a bare list — it crashed with `AttributeError: 'list' object has no attribute 'get'`.
- *What I changed:* Added a type check: `wardrobe.get("items", []) if isinstance(wardrobe, dict) else wardrobe`, so both a bare list and a `{"items": [...]}` dict are accepted.

**Moment 2**

- *What I asked for:* I asked Claude to implement `search_listings` per my spec, with the size filter handling messy sizes like "W30 L30", "S/M", and "XL (oversized)".
- *What came back:* The initial `search_listings` used a plain `"s" in listing_size.lower()` substring check. Tested with size "S", it also matched listings with size "US 7" and "XL (oversized)" because "s" is a substring of both.
- *What I changed:* Replaced the substring check with a token-based approach: split both the query size and listing size on spaces, slashes, and parentheses, then check for any shared token. "S" now only matches listings whose size tokenizes to include "S" exactly.

**Unit 4 Moment**

- *What I asked for:* After seeing criterion 4 MISSED (only 1 of 5 fit cards had a distinct opening), I asked Claude to diagnose why the model kept producing "Scored this..." as the opener on every run.
- *What came back:* Claude identified two converging factors: (1) the same item was returned deterministically every run because the size M filter eliminated most jackets, leaving the bucket hat as the consistent top result; (2) the `create_fit_card` prompt had no instruction about structure, so the model defaulted to its best guess at a canonical thrift caption opener. The diagnosis pointed at the prompt, not the tool or loop.
- *What I changed:* Added an explicit negative constraint ("Do NOT open with 'Scored this' or any variant of it") and a positive direction (start from the vibe, a styling moment, what makes the piece interesting, or the deal) to the prompt in `tools.py::create_fit_card`. After the change, all 5 fit cards in the after run had distinct openings and none started with "Scored this".

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Failure Modes

All three failure modes triggered manually. Commands and real output below.

**1. Empty search** -- query that matches nothing

```
$ python app.py ask 'neon green snowsuit under $5'

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch: empty results
      →    stopping — no listings matched

  No listings matched your search for 'neon green snowsuit'. Try broadening your keywords, or adjusting your size or price ceiling ($5).
```

**2. Empty wardrobe** -- user with nothing saved

```
$ python app.py ask 'vintage graphic tee under $30' --empty-wardrobe
(running with an empty wardrobe)

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: Since you are starting from scratch without a saved wardrobe yet, the best way to style a Y2K baby tee is to i…
[5] create_fit_card
      in:  dict with keys: item
      out: Butterflies, pastels, and a major Y2K model-off-duty moment for just $18 on Depop. Pairing this little baby te…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Since you are starting from scratch without a saved wardrobe yet, the best way to style a Y2K baby tee
            is to invest in a few foundational staple pieces...

  Fit card: Butterflies, pastels, and a major Y2K model-off-duty moment for just $18 on Depop. Pairing this little
            baby tee with some baggy low-rise denim is about to be my entire personality this season.
```

The agent ran to completion with general styling advice instead of wardrobe-specific outfits. No crash.

**3. Model unavailable** -- bad API key

```
$ python app.py ask 'corduroy pants under $40'
# (run with one character of GEMINI_API_KEY changed)

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 2 items: Corduroy Wide-Leg Pants — Rust, Low-Rise Cargo Pants — Khaki
[3] select_item
      out: Corduroy Wide-Leg Pants — Rust ($32.0, depop)
[4] suggest_outfit
      →    ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

  The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

1 model calls this session
```

The agent ran parse_query, search_listings, and select_item successfully before hitting the model call in suggest_outfit. `ModelUnavailable` was caught in `agent.py::run_agent` and surfaced as a plain error message. No stack trace shown to the user.

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

Source: `results/run_2026-10-09_2338_before.md`, loop: `agent.py::run_agent`

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes all 3 tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops before suggest_outfit | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item id matches suggest_outfit input | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card: title mention + under 100 words + distinct opening | 5/5 | PASS | FAIL | FAIL | FAIL | FAIL | MISSED (1/5 distinct openings) |
| 5. every search result respects price ceiling | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Criterion 4 note: title mention and word count passed all 5 tries. The failure was on distinct openings -- tries 2-5 all opened with "Scored this reversible brown plaid bucket hat on thredUp for just $14". Only try 1 had a distinct opener. 1/5 distinct, need 4/5.

**Real output from one try**, pasted as text, naming the file and function
that produced it:

File: `results/run_2026-10-09_2338_before.md` | Loop: `agent.py::run_agent`
Scenario: matching query completes | Query: `vintage graphic tee under $30` | Try 1

```
- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Fit card:
Scored this butterfly baby tee on Depop for $18 and I'm obsessed 🦋 Already styling it three
ways—from baggy denim to combat boots—because we are fully leaning into the 2000s aesthetic
this week. Which look is your favorite?

Trace:
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: Here are 3 specific outfit ideas that pair the new Y2K butterfly baby tee with pieces from your current wardro…
[5] create_fit_card
      in:  dict with keys: item
      out: Scored this butterfly baby tee on Depop for $18 and I'm obsessed 🦋 Already styling it three ways—from baggy de…
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | matching query completes all 3 tools | 4/5 | MET | 5 of 5 runs completed all 5 trace steps (parse_query -> search_listings -> select_item -> suggest_outfit -> create_fit_card) with no early stop. |
| 2 | impossible query stops before suggest_outfit | 5/5 | MET | All 5 runs hit the empty-results branch and stopped at trace step [3]. No suggest_outfit or create_fit_card call appeared in any trace. |
| 3 | selected_item id matches suggest_outfit input | 5/5 | MET | The assert in run_agent passed on every run; no AssertionError appeared in any trace output. |
| 4 | fit card: title mention + under 100 words + distinct opening | 5/5 | MISSED | Title mention and word count passed all 5 tries. But 4 of 5 fit cards opened with the same sentence: "Scored this reversible brown plaid bucket hat on thredUp for just $14". Only try 1 was distinct. 1/5 distinct; target is 4/5. |
| 5 | every search result respects price ceiling | 5/5 | MET | Every item price in each run was at or below the query's max_price. The price filter runs before the keyword scorer, so no over-budget item can slip through. |

**Diagnoses**

Criterion 4 miss: the failure was in the model's output layer, not in the tool or loop branch. The search tool returned the same item deterministically on all 5 runs: Bucket Hat -- Reversible, Brown Plaid at $14 on thredUp. That happened because the "90s track jacket, size M" query's size M filter eliminated most actual jackets, leaving only accessories; the keyword scorer then surfaced the bucket hat (which carries "90s" in its style tags) as the top result. With the same item in every create_fit_card call, and no prompt constraint on structure, the model converged to its canonical thrift caption opener: "Scored this [item] on [platform] for just $[price]". The tool, loop branch, and session state all worked correctly. The prompt was missing a constraint.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

Source: `results/run_2026-10-09_2338_before.md` | Loop: `agent.py::run_agent`

**Happy path** (query: `vintage graphic tee under $30, size M`)

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: item, wardrobe_items
      out: Here are 3 specific outfit ideas that pair the new Y2K butterfly baby tee with pieces from your current wardro…
[5] create_fit_card
      in:  dict with keys: item
      out: Scored this butterfly baby tee on Depop for $18 and I'm obsessed 🦋 Already styling it three ways—from baggy de…
```

**Empty search** (query: `neon green snowsuit under $5, size XL`)

```
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch: empty results
      ->   stopping — no listings matched
```

Step [2] in both traces shows `(via MCP)` because `search_listings` now runs inside `mcp_server.py` and the agent calls it through `mcp_client.call_tool`. The 5-step trace (happy path) is visibly longer than the 3-step trace (empty search), confirming the branch fires and stops early.

**On the MCP move:** In `agent.py`, the direct `from tools import search_listings` import was removed. The call was replaced with `mcp_client.call_tool("search_listings", {"description": ..., "size": ..., "max_price": ...})`. Inside `mcp_client.py`, `call_tool` starts `mcp_server.py` as a subprocess over stdio, sends a JSON-RPC request, and returns the result. The tool logic in `tools.py` did not change at all -- only the transport layer changed. Behavior was identical before and after the move: same results, same trace output.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** Added two instructions to the `create_fit_card` prompt in `tools.py`: (1) a negative constraint -- "Do NOT open with 'Scored this' or any variant of it", and (2) a positive direction -- start from the vibe it unlocks, a specific styling moment, what makes the piece interesting, or the deal itself. No other code changed.

**Which failure it was meant to fix:** Criterion 4, distinct openings. The diagnosis pointed at the model's output layer: the prompt had no constraint on how a caption should open, so the model defaulted to the same opener every run. Adding a negative constraint directly targets that failure mechanism.

### Run Log — After

Source: `results/run_2026-10-09_2353_after.md`, loop: `agent.py::run_agent`

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes all 3 tools | 4/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops before suggest_outfit | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. selected_item id matches suggest_outfit input | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. fit card: title mention + under 100 words + distinct opening | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. every search result respects price ceiling | 5/5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes. Criterion 4 moved from MISSED (1/5 distinct) to MET (5/5 distinct). The 5 after-run fit cards opened with: (1) "The 90s streetwear energy this brown plaid bucket hat brings is unmatched..." (2) "That 90s streetwear energy just unlocked a whole new level of cozy layering..." (3) "Found this reversible brown plaid bucket hat on thredUp for just $14..." (4) "14 bucks on thredUp for a reversible brown plaid bucket hat..." (5) "The ultimate 90s streetwear cheat code is officially this reversible brown plaid bucket hat..." None started with "Scored this". All 5 are distinct. All other criteria stayed MET.

---

## What's Still Broken

**Scenario mismatch in criterion 4:** Criterion 4 as written tests 5 different items, but the eval scenario ran one item (the bucket hat) five times. That is a stricter test of opener variety on one item, not what the criterion says. The after-run MET result also rests on one item, so it shows the prompt change works on that item, not that distinctness is solved in general. Properly testing criterion 4 would require five scenarios with five different matching queries, each returning a different top item.

**Search relevance:** The "90s track jacket, size M" query used in criterion 4 still returns a bucket hat as the top result. The size M filter removes most actual jackets from the pool, and the keyword scorer matches "90s" in the bucket hat's style tags. This is a search relevance issue: the tool returns valid items (they exist, their price is fine, size matches), but the category is wrong. Fixing it would require a category filter in the query parser, a category-weighted scorer, or a semantic re-ranking step. No current criterion fails because of this -- criterion 4 tests fit card quality, not result relevance -- so it was left unfixed.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

## Data Notes
- Listing fields: id, title, description, category, style_tags (list), size (str), condition, price (float), colors (list), brand (can be null), platform
- Sizes are messy strings ("W30 L30", "S/M", "XL (oversized)", "M"), so size matching can't be a plain equality check
- Wardrobe item fields: id, name, category, colors, style_tags, notes
