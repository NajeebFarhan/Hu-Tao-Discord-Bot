import subprocess
import signal
import sys
from watchfiles import watch

process = None


def start_process():
    return subprocess.Popen(
        ["uv", "run", "src/bot.py"],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        if sys.platform == "win32"
        else 0,
    )


def stop_process(proc):
    if proc and proc.poll() is None:
        print("Stopping old process...")
        if sys.platform == "win32":
            proc.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            proc.send_signal(signal.SIGINT)
        proc.wait()


if __name__ == "__main__":
    process = start_process()

    for changes in watch("./src", recursive=True):
        print("File change detected. Reloading...")
        stop_process(process)
        process = start_process()