import os
import json
import shutil
from .core import LOG_FILE


def restore(folder):
    """
    Restore files to their original locations using the organize log file.
    
    Args:
        folder (str): Path to the folder containing the log file
        
    Raises:
        ValueError: If folder doesn't exist
        IOError: If log file cannot be read
    """
    if not os.path.exists(folder):
        raise ValueError(f"Folder does not exist: {folder}")
    
    log_path = os.path.join(folder, LOG_FILE)

    if not os.path.exists(log_path):
        print("❌ No log file found.")
        return

    try:
        with open(log_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Log file is corrupted: {str(e)}")
        return
    except IOError as e:
        print(f"❌ Error: Cannot read log file: {str(e)}")
        return

    if "moves" not in data or not isinstance(data["moves"], list):
        print("❌ Error: Log file has invalid format")
        return

    restored_count = 0
    failed_count = 0

    for move in reversed(data["moves"]):
        # Validate move entry
        if "from" not in move or "to" not in move:
            print(f"⚠ Skipping invalid log entry: {move}")
            failed_count += 1
            continue
            
        if not os.path.exists(move["to"]):
            print(f"⚠ Source file not found: {move['to']}")
            failed_count += 1
            continue

        try:
            # Create original directory if it doesn't exist
            os.makedirs(os.path.dirname(move["from"]), exist_ok=True)
            # Move file back to original location
            shutil.move(move["to"], move["from"])
            print(f"↩ restored → {move['from']}")
            restored_count += 1
        except (PermissionError, OSError) as e:
            print(f"⚠ Could not restore {move['to']}: {str(e)}")
            failed_count += 1

    print(f"✅ Restore complete. Restored: {restored_count}, Failed: {failed_count}")

