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

- *What I asked for:*
- *What came back:* The initial `search_listings` used a plain `"s" in listing_size.lower()` substring check. Tested with size "S", it also matched listings with size "US 7" and "XL (oversized)" because "s" is a substring of both.
- *What I changed:* Replaced the substring check with a token-based approach: split both the query size and listing size on spaces, slashes, and parentheses, then check for any shared token. "S" now only matches listings whose size tokenizes to include "S" exactly.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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
