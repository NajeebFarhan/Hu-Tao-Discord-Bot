from discord.ext import commands
from .chat import chat
from .ping import ping
from .delete_msg import deletechat, deleteall
from .history import history


COMMANDS: list[commands.Command] = [chat, ping, deletechat, deleteall, history]