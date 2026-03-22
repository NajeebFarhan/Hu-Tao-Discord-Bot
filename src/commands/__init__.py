from discord.ext import commands
from .chat import chat
from .ping import ping
from .delete_msg import deletemsg, deleteall


COMMANDS: list[commands.Command] = [chat, ping, deletemsg, deleteall]