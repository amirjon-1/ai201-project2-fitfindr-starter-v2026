"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


def _size_tokens(size_str: str) -> set[str]:
    """Split a size string into tokens for flexible matching."""
    return {t.upper() for t in re.split(r'[\s/()\-]+', size_str) if t}


def _size_matches(query_size: str, listing_size: str) -> bool:
    """Return True if query_size appears as a whole token in listing_size."""
    listing_tokens = _size_tokens(listing_size)
    query_tokens = _size_tokens(query_size)
    return bool(query_tokens & listing_tokens)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.
    """
    listings = load_listings()

    if max_price is not None:
        listings = [l for l in listings if l["price"] <= max_price]

    if size is not None:
        listings = [l for l in listings if _size_matches(size, l["size"])]

    keywords = [kw.lower() for kw in re.split(r'\s+', description.strip()) if kw]

    def score(listing: dict) -> int:
        searchable = " ".join([
            listing.get("title", ""),
            listing.get("description", ""),
            " ".join(listing.get("style_tags", [])),
        ]).lower()
        return sum(1 for kw in keywords if kw in searchable)

    scored = [(score(l), l) for l in listings]
    scored = [(s, l) for s, l in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [l for _, l in scored[:config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  May be empty.

    Returns:
        A non-empty string with outfit suggestions, or general styling advice
        when wardrobe is empty.
    """
    item_desc = (
        f"{new_item.get('title', 'item')} "
        f"({new_item.get('category', '')}, size {new_item.get('size', '')}, "
        f"colors: {', '.join(new_item.get('colors', []))}, "
        f"style: {', '.join(new_item.get('style_tags', []))})"
    )

    wardrobe_items = wardrobe.get("items", []) if isinstance(wardrobe, dict) else wardrobe

    if not wardrobe_items:
        prompt = (
            f"I'm considering buying this thrifted item: {item_desc}.\n"
            "I don't have a saved wardrobe yet. Give me 2-3 outfit ideas "
            "showing how to style this piece — mention specific types of basics "
            "or staple pieces that would pair well with it."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {w.get('name', '')} ({w.get('category', '')}, "
            f"colors: {', '.join(w.get('colors', []))})"
            for w in wardrobe_items
        )
        prompt = (
            f"I'm considering buying this thrifted item: {item_desc}.\n\n"
            f"My current wardrobe:\n{wardrobe_lines}\n\n"
            "Suggest 2-3 specific outfits that pair this new item with pieces "
            "I already own. Name the exact wardrobe pieces in each outfit."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A 1-3 sentence caption, or "" if outfit is empty/whitespace.
    """
    if not outfit or not outfit.strip():
        return ""

    title = new_item.get("title", "this thrifted find")
    price = new_item.get("price", "")
    platform = new_item.get("platform", "")
    brand = new_item.get("brand")

    item_ref = f"{brand} {title}" if brand else title
    price_platform = f"${price} on {platform}" if price and platform else ""

    prompt = (
        f"Write a 1-3 sentence social media caption for this thrift find.\n\n"
        f"Item: {item_ref}"
        + (f", found for {price_platform}" if price_platform else "")
        + f"\nOutfit idea: {outfit}\n\n"
        "Make it sound like something a real person would post — casual, "
        "specific about the vibe, not a product description. Mention the item "
        "and its price and platform once."
    )

    return generate(prompt)
