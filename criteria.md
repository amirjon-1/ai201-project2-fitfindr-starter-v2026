# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
4 of 5 because search is a plain keyword match and some phrasings will miss, and two of the three tools call a model that can fail or return something unusable.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
5 of 5 because this path is pure code: an empty list triggers the branch, and no model is involved before the stop.

---
## 3. Something about state

Across 5 runs of a matching query, the `id` in `session["selected_item"]` is identical to the `id` of the item passed into `suggest_outfit`, checked by an assert inside `run_agent` — 5 of 5.

**Why this target:** The item has to stay consistent from search to outfit suggestion, or the outfit is for the wrong thing. Both values come from code I control, with no model in between, so nothing should vary and anything below 5 of 5 is a bug.

---

## 4. Something about the fit card

For 5 different matching items, each fit card (a) mentions the item by title or a key word from the title, and (b) is under 100 words — 5 of 5 for both. Across the 5 cards, no more than 1 shares an opening sentence with another card — at least 4 of 5 distinct.

**Why this target:** The card must be clearly about the selected item and short enough to post. I don't require identical wording run to run because the model is meant to vary. The opening-sentence check is 4 of 5 rather than 5 of 5 because the model may occasionally fall into a generic opener, and that's the one thing I want measured.

---

## 5. Every result respects the price ceiling

For 5 queries that each include a max price (e.g. "under $30"), every listing returned by `search_listings` has `price <= max_price` — 5 of 5.

**Why this target:** A result over the user's stated budget is unusable. The check is a plain numeric comparison on the listing's `price` field, with no model involved, so it should never miss.
---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
