import subprocess
import os
import signal
from watchfiles import watch

process = None

def start():
    global process
    process = subprocess.Popen(
        ["uv", "run", "src/bot.py"],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )

def stop():
    global process
    if process and process.poll() is None:
        process.send_signal(signal.CTRL_BREAK_EVENT)
        process.wait()

if __name__ == "__main__":
    start()
    for _ in watch("."):
        print("Change detected. Restarting...")
        stop()
        start()