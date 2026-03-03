dev:
    uv run dev.py

run:
    uv run src/bot.py


lint:
    uvx ruff check .

format:
    uvx ruff format .