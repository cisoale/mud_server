import subprocess
import time

while True:
    print("🚀 Avvio server...")
    
    process = subprocess.Popen(["python", "main.py"])
    
    process.wait()

    print("💀 Server crashato, riavvio tra 2 secondi...")
    time.sleep(2)