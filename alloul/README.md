# ALLOUL Browser Agent

Gulf/UAE market research layer built on top of the browser-use fork.
Powers the alloul.OT AdEngine service.

## What it does

- Runs browser automation tasks using Groq (llama-3.3-70b) for speed
- Falls back to Claude Sonnet for complex visual/screenshot reasoning
- Launches Chromium with UAE Arabic locale and Dubai timezone
- Provides five prebuilt Gulf research skills: competitor ads, market trends,
  hashtag research, price checks, and ad inspiration lookups

## Available research tasks

| Task name | Parameters |
|---|---|
| `competitor_ads` | `brand`, `industry` |
| `market_trends` | `industry` |
| `hashtag_research` | `topic` |
| `price_check` | `product`, `city` (default: Dubai) |
| `ad_inspiration` | `industry` |

## Run the API

```bash
pip install -r alloul/requirements.txt
GROQ_API_KEY=<your-key> python -m alloul.api
# Listens on http://0.0.0.0:8002
```

## Quick example

```python
import asyncio
from alloul.skills.gulf_research import research

result = asyncio.run(research("price_check", product="iPhone 15", city="Abu Dhabi"))
print(result)
```

## Environment variables

- `GROQ_API_KEY` — Groq API key (required for fast mode)
- `ANTHROPIC_API_KEY` — Claude key (required when `fast=False`)
