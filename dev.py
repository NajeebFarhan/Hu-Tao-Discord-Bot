# import subprocess
# import os
# import signal

# process = None

# def start():
#     stop()
#     global process
#     process = subprocess.Popen(
#         ["uv", "run", "src/bot.py"],
#         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
#     )

# def stop():
#     global process
#     if process:
#         process.send_signal(signal.CTRL_BREAK_EVENT)
#         process.wait()

# if __name__ == "__main__":
#     start()