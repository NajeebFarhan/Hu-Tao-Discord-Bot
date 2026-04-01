from discord.ext import commands
from .chat import chat
from .ping import ping
from .delete_msg import deletechat, deleteall
from .history import history
from .generate_openai_key import gen_openai_key

COMMANDS: list[commands.Command] = [chat, ping, deletechat, deleteall, history, gen_openai_key]