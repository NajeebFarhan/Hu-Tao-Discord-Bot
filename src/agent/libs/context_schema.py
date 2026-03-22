from dataclasses import dataclass
import discord

@dataclass
class Context:
    user_id: int
    prompt: str
    attachments: list[discord.Attachment]