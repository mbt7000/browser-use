"""Gulf market research skills for ALLOUL AdEngine."""
import asyncio

from alloul.agent import run_task

RESEARCH_TASKS = {
    "competitor_ads": lambda brand, industry: f"""
        Go to Meta Ad Library at https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AE&q={brand}&search_type=keyword_unordered
        Find the top 5 active ads for '{brand}' in UAE.
        For each ad extract: headline, main message, call to action, visual style.
        Return as JSON list.
    """,

    "market_trends": lambda industry: f"""
        Search Google for '{industry} market trends UAE 2025 site:dubizzle.com OR site:bayut.com OR site:zawya.com'.
        Extract key trends, growth numbers, and popular segments.
        Return a summary in Arabic and English.
    """,

    "hashtag_research": lambda topic: f"""
        Go to https://www.instagram.com/explore/tags/{topic.replace(' ', '')}/
        Count the posts and note related hashtags shown.
        Also search Twitter/X for trending {topic} hashtags in UAE.
        Return top 10 Arabic hashtags and top 10 English hashtags.
    """,

    "price_check": lambda product, city="Dubai": f"""
        Search for '{product} price {city}' on Google Shopping and dubizzle.com.
        Extract: minimum price, maximum price, average price, currency (AED).
        Return as JSON with these fields.
    """,

    "ad_inspiration": lambda industry: f"""
        Search Google Images for '{industry} advertisement UAE Arabic'
        and 'إعلان {industry} الإمارات'.
        Note the visual styles, colors, and messages used.
        Return description of 5 best ad styles found.
    """,
}


async def research(task_name: str, **kwargs) -> str:
    """Run a named research task with given parameters."""
    if task_name not in RESEARCH_TASKS:
        raise ValueError(f"Unknown task: {task_name}. Available: {list(RESEARCH_TASKS.keys())}")

    task_fn = RESEARCH_TASKS[task_name]
    task = task_fn(**kwargs)
    return await run_task(task.strip(), fast=True, max_steps=8)


async def run_parallel_research(tasks: list[dict]) -> list[str]:
    """Run multiple research tasks in parallel."""
    coroutines = [research(t["task"], **t.get("kwargs", {})) for t in tasks]
    return await asyncio.gather(*coroutines, return_exceptions=True)
