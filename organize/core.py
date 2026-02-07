import os, shutil, hashlib, json
from datetime import datetime
from .filetypes import FILE_TYPES

LOG_FILE = ".organize_log.json"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def category(ext):
    for k, v in FILE_TYPES.items():
        if ext in v:
            return k
    return "Others"


def safe_move(src, dest):
    os.makedirs(dest, exist_ok=True)
    base, ext = os.path.splitext(os.path.basename(src))
    new = os.path.join(dest, base + ext)

    i = 1
    while os.path.exists(new):
        new = os.path.join(dest, f"{base}({i}){ext}")
        i += 1

    shutil.move(src, new)
    return new


def organize(folder, dry_run=False):
    seen = {}
    log = []

    for root, _, files in os.walk(folder):
        for f in files:
            if f == LOG_FILE:
                continue

            src = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            ext = ext.lower()

            cat = category(ext)
            dest_dir = os.path.join(folder, cat)

            try:
                h = sha256(src)
            except Exception:
                continue

            if h in seen:
                print(f"🗑 duplicate → {src}")
                if not dry_run:
                    os.remove(src)
                continue
            seen[h] = src

            if os.path.dirname(src) == dest_dir:
                continue

            print(f"📁 {src} → {cat}")

            if not dry_run:
                new_path = safe_move(src, dest_dir)
                log.append({"from": src, "to": new_path})

    if not dry_run and log:
        with open(os.path.join(folder, LOG_FILE), "w") as f:
            json.dump({"timestamp": datetime.now().isoformat(), "moves": log}, f, indent=2)
