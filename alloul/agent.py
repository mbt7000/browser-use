"""
ALLOUL Browser Agent — optimized for Gulf market research.
Uses ChatGroq (llama-3.3-70b) for fast decision-making.
"""
import asyncio
import os

from browser_use import Agent, ChatAnthropic, ChatGroq
from browser_use.browser import BrowserProfile

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise EnvironmentError("GROQ_API_KEY environment variable is required")


def get_llm(fast: bool = True):
    """Returns ChatGroq for fast tasks, ChatAnthropic for complex ones."""
    if fast:
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=GROQ_KEY,
        )
    # Claude for complex visual reasoning (screenshots)
    return ChatAnthropic(model="claude-sonnet-4-6")


def get_gulf_profile() -> BrowserProfile:
    """Browser profile optimized for Gulf/Arabic websites."""
    return BrowserProfile(
        headless=True,
        # Set UAE Arabic user-agent to signal language/region to servers
        user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        ),
        # Chromium launch args that configure locale and timezone at process level
        args=[
            "--lang=ar-AE",
            "--accept-lang=ar-AE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "--timezone=Asia/Dubai",
        ],
    )


async def run_task(task: str, fast: bool = True, max_steps: int = 10) -> str:
    """Run a browser task and return the result as a string."""
    llm = get_llm(fast=fast)
    profile = get_gulf_profile()

    agent = Agent(
        task=task,
        llm=llm,
        browser_profile=profile,
        max_steps=max_steps,
    )

    result = await agent.run()
    return str(result.final_result() or "")


if __name__ == "__main__":
    result = asyncio.run(run_task("ابحث عن أسعار إعلانات Meta في الإمارات"))
    print(result)
