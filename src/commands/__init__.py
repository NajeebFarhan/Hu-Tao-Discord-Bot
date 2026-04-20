from discord.ext import commands
from .chat import chat
from .ping import ping
from .delete_msg import deletechat, deleteall
from .history import history, view
from .channel import channel
from .generate_openai_key import gen_openai_key
from .remote_chat import remote_chat, remote_reply, remote_edit, remote_delete, remote_delete_last, remote_pin, remote_reaction

COMMANDS: list[commands.Command] = [chat, ping, deletechat, deleteall, history, view, channel, gen_openai_key, remote_chat, remote_reply, remote_edit, remote_delete, remote_delete_last, remote_pin, remote_reaction]