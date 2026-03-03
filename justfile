dev:
    watchfiles uv run src.bot:main

run:
    uv run python src/bot.py


lint:
    uvx ruff check .

format:
    uvx ruff format .