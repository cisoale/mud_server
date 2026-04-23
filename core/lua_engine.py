import subprocess
import json

LUA_CMD = "lua54"

def run_lua(script_path, context=None):

    try:
        input_data = json.dumps(context or {})

        result = subprocess.run(
            [LUA_CMD, script_path],
            input=input_data,
            text=True,
            capture_output=True
        )

        if result.stderr:
            print("[LUA ERROR]", result.stderr)

        return result.stdout.strip()

    except Exception as e:
        print("[LUA ENGINE ERROR]", e)
        return None