##################
# This is an april fools commands
#
##################

import discord
from discord.ext import commands
import asyncio
import random


fake_keys = [
    "sk-live-touch-grass-required",
    "sk-prod-go-outside-v1",
    "sk-dev-main-character-energy",
    "sk-live-npc-behavior-detected",
    "sk-prod-skill-issue-found",
    "sk-live-loading-social-life",
    "sk-dev-update-your-vibes",
    "sk-prod-battery-low-energy",
    "sk-live-please-stand-up",
    "sk-prod-reality-check-needed",

    "sk-prod-no-rizz-detected",
    "sk-live-zero-aura-build",
    "sk-prod-delulu-mode-enabled",
    "sk-dev-sigma-but-confused",
    "sk-live-gyatt-level-error",
    "sk-prod-fanum-tax-required",
    "sk-live-skibidi-permission-denied",
    "sk-dev-brainrot-v3",
    "sk-prod-npc-dialogue-loop",
    "sk-live-aura-farming-failed",

    # "sk-live-404-social-skills",
    # "sk-prod-outside-not-found",
    # "sk-dev-try-again-tomorrow",
    # "sk-live-coffee-required",
    # "sk-prod-sleep-deprived-build",
    # "sk-live-too-many-tabs-open",
    # "sk-prod-thinking-too-hard",
    # "sk-dev-error-just-vibing",
    # "sk-live-procrastination-pro",
    # "sk-prod-weekend-when",

    "sk-live-skibidi-rizz-pro-max",
    "sk-prod-ohio-final-boss",
    "sk-live-rizz-training-failed",
    "sk-dev-sigma-mindset-beta",
    "sk-prod-brainrot-overflow",
    "sk-live-just-one-more-video",
    "sk-dev-infinite-scroll-enabled",
    "sk-prod-vibes-not-found",
    "sk-live-lagging-in-real-life",
    "sk-dev-too-much-internet",

    # "sk-prod-almost-productivity",
    # "sk-live-focus-mode-failed",
    # "sk-dev-potential-loading",
    # "sk-prod-success-coming-soon",
    # "sk-live-legend-in-progress",
    # "sk-prod-confidence-beta",
    # "sk-live-learning-arc-active",
    # "sk-dev-glowup-pending",
    # "sk-prod-future-op-build",
    # "sk-live-upgrade-yourself",

    "sk-prod-npc-energy-detected",
    "sk-live-background-character-mode",
    "sk-dev-cutscene-skipped",
    "sk-prod-side-quest-enjoyer",
    "sk-live-fast-travel-unlocked",
    "sk-dev-low-stamina-build",
    "sk-prod-cutscene-in-real-life",
    "sk-live-story-arc-loading",
    "sk-dev-main-quest-ignored",
    "sk-prod-level-up-pending",

    "sk-live-bing-chilling-energy",
    "sk-prod-ohio-certified",
    "sk-dev-sus-level-max",
    "sk-live-amogus-detected",
    "sk-prod-imposter-syndrome-v2",
    "sk-dev-vibe-check-failed",
    "sk-live-caught-in-4k",
    "sk-prod-cringe-detected",
    "sk-dev-based-but-lost",
    "sk-live-mid-response-generated",

    # "sk-prod-low-motivation-build",
    # "sk-live-brain-loading",
    # "sk-dev-memory-leak-energy",
    # "sk-prod-no-thoughts-head-empty",
    # "sk-live-confused-screaming",
    # "sk-dev-error-thinking",
    # "sk-prod-processing-life",
    # "sk-live-buffering-reality",
    # "sk-dev-existential-lag",
    # "sk-prod-consciousness-beta",

    # "sk-live-too-many-thoughts",
    # "sk-prod-not-enough-sleep",
    # "sk-dev-monday-again",
    # "sk-live-weekend-loading",
    # "sk-prod-time-fast-forward",
    # "sk-dev-life-speedrun",
    # "sk-live-late-again-build",
    # "sk-prod-alarm-snoozed-v7",
    # "sk-dev-five-more-minutes",
    # "sk-live-running-on-coffee",

    # "sk-prod-chaos-engine-enabled",
    # "sk-live-random-thought-generator",
    # "sk-dev-unexpected-behavior",
    # "sk-prod-glitch-in-matrix",
    # "sk-live-parallel-universe-mode",
    # "sk-dev-bug-or-feature",
    # "sk-prod-unpatched-human",
    # "sk-live-debugging-life",
    # "sk-dev-reality-runtime-error",
    # "sk-prod-simulation-suspected",

    # "sk-live-fake-it-till-working",
    # "sk-prod-confidence-overflow",
    # "sk-dev-overthinking-v5",
    # "sk-live-social-battery-empty",
    # "sk-prod-introvert-pro-max",
    # "sk-dev-extrovert-trial-version",
    # "sk-live-human-update-needed",
    # "sk-prod-character-development",
    # "sk-dev-emotional-damage-lite",
    # "sk-live-personality-loading"
]


@commands.command(name="gengptkey")
async def gen_openai_key(ctx: commands.Context):
    
    # Step 1 — initial message
    msg = await ctx.send("🔐 Generating OpenAI API key...")

    # Step 2 — fake loading delay
    await asyncio.sleep(random.uniform(2.5, 4.5))

    # Step 3 — choose fake key
    fake_key: str = random.choice(fake_keys)

    # Step 4 — DM the user
    try:
        dm_channel = await ctx.author.create_dm()
            
        await dm_channel.send(
            f"🔑 **Your OpenAI API key:**\n\n"
            f"`{fake_key}`"
        )

        # Step 5 — confirm in server
        await msg.edit(
            content=(
                "✅ Your ChatGPT API key has been sent to your DM.\n"
                "⚠️ Keep your API key secure. Do not share it publicly."
            )
        )
        
        await asyncio.sleep(5)
        await dm_channel.send("https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713")

    except discord.Forbidden:
        await msg.edit(
            content="❌ I couldn't DM you. Please enable DMs from server members."
        )