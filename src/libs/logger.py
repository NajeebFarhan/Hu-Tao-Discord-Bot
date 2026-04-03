import logging

logger = logging.getLogger("discord")

def log_command_error(ctx, error: Exception):
    """
    Logs a command error with useful Discord context.
    """
    logger.exception(
        "Command error | "
        f"command={ctx.command} | "
        f"user={ctx.author} (id={ctx.author.id}) | "
        f"guild={getattr(ctx.guild, 'name', 'DM')} (id={getattr(ctx.guild, 'id', 'DM')}) | "
        f"channel={ctx.channel} (id={ctx.channel.id})",
        exc_info=error
    )