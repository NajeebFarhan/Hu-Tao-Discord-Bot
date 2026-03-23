from discord.ext import commands
from .chat import chat
from .ping import ping
from .delete_msg import deletemsg, deleteall
from .history import history


COMMANDS: list[commands.Command] = [chat, ping, deletemsg, deleteall, history]