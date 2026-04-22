import subprocess
import time
import os

LAST_MOD = 0

def get_last_modified():
    latest = 0
    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                mtime = os.path.getmtime(path)
                if mtime > latest:
                    latest = mtime
    return latest


while True:
    LAST_MOD = get_last_modified()

    print("🚀 Avvio server...")
    process = subprocess.Popen(["python", "main.py"])

    while True:
        time.sleep(1)

        current = get_last_modified()

        if current > LAST_MOD:
            print("🔄 Modifica rilevata, riavvio server...")
            process.kill()
            break

        if process.poll() is not None:
            print("💀 Crash rilevato, riavvio...")
            break