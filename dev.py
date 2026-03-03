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
        print("Stopping process...")
        try:
            if sys.platform == "win32":
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                proc.send_signal(signal.SIGINT)
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Force killing...")
            proc.kill()


if __name__ == "__main__":
    try:
        process = start_process()

        for _ in watch("./src/"):
            print("File change detected. Reloading...")
            stop_process(process)
            process = start_process()

    except KeyboardInterrupt:
        print("\nShutting down dev server...")
        stop_process(process)

    finally:
        sys.exit(0)