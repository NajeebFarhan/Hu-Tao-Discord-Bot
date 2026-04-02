from discord.ext import commands
from .chat import chat
from .ping import ping
from .delete_msg import deletechat, deleteall
from .history import history
from .channel import channel
from .generate_openai_key import gen_openai_key

COMMANDS: list[commands.Command] = [chat, ping, deletechat, deleteall, history, channel, gen_openai_key]