import os, json, shutil
from .core import LOG_FILE


def restore(folder):
    log_path = os.path.join(folder, LOG_FILE)

    if not os.path.exists(log_path):
        print("❌ No log file found.")
        return

    with open(log_path) as f:
        data = json.load(f)

    for move in reversed(data["moves"]):
        if os.path.exists(move["to"]):
            os.makedirs(os.path.dirname(move["from"]), exist_ok=True)
            shutil.move(move["to"], move["from"])
            print(f"↩ restored → {move['from']}")

    print("✅ Restore complete.")
