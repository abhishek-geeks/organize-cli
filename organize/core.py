import os, shutil, hashlib, json
from datetime import datetime
from .filetypes import FILE_TYPES

LOG_FILE = ".organize_log.json"


def sha256(path):
    """
    Calculate SHA-256 hash of a file.
    
    Args:
        path (str): Path to the file
        
    Returns:
        str: Hexadecimal SHA-256 hash
        
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
        IOError: If there's an error reading the file
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Cannot read file: {path} (permission denied)")
    
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except IOError as e:
        raise IOError(f"Error reading file {path}: {str(e)}")


def category(ext):
    """
    Categorize a file based on its extension.
    
    Args:
        ext (str): File extension (e.g., '.pdf', '.mp3')
        
    Returns:
        str: Category name (Audio, Video, Images, etc.) or 'Others' if unknown
    """
    ext = ext.lower()  # Convert to lowercase for case-insensitive matching
    for k, v in FILE_TYPES.items():
        if ext in v:
            return k
    return "Others"


def safe_move(src, dest):
    """
    Move a file to destination, handling naming conflicts.
    
    Args:
        src (str): Source file path
        dest (str): Destination directory path
        
    Returns:
        str: New path of the moved file
        
    Raises:
        FileNotFoundError: If source file doesn't exist
        PermissionError: If cannot move file
        OSError: If there's an error during move
    """
    if not os.path.exists(src):
        raise FileNotFoundError(f"Source file not found: {src}")
    
    try:
        os.makedirs(dest, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"Cannot create directory: {dest} (permission denied)")
    except OSError as e:
        raise OSError(f"Error creating directory {dest}: {str(e)}")
    
    base, ext = os.path.splitext(os.path.basename(src))
    new = os.path.join(dest, base + ext)

    i = 1
    while os.path.exists(new):
        new = os.path.join(dest, f"{base}({i}){ext}")
        i += 1

    try:
        shutil.move(src, new)
        return new
    except PermissionError:
        raise PermissionError(f"Cannot move file {src} to {dest} (permission denied)")
    except OSError as e:
        raise OSError(f"Error moving file from {src} to {new}: {str(e)}")


def organize(folder, dry_run=False):
    """
    Organize files in a folder by categorizing them into subdirectories.
    
    Args:
        folder (str): Path to the folder to organize
        dry_run (bool): If True, preview changes without making them
        
    Raises:
        ValueError: If folder doesn't exist
        PermissionError: If folder cannot be accessed
        OSError: If there's an error during organization
    """
    if not os.path.exists(folder):
        raise ValueError(f"Folder does not exist: {folder}")
    
    if not os.path.isdir(folder):
        raise ValueError(f"Path is not a directory: {folder}")
    
    if not os.access(folder, os.R_OK):
        raise PermissionError(f"Cannot read folder: {folder} (permission denied)")
    
    seen = {}
    log = []
    skipped = 0

    for root, _, files in os.walk(folder):
        for f in files:
            if f == LOG_FILE:
                continue

            src = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            ext = ext.lower()

            cat = category(ext)
            dest_dir = os.path.join(folder, cat)

            # Try to hash the file, skip if there's an error
            try:
                h = sha256(src)
            except (FileNotFoundError, PermissionError, IOError) as e:
                print(f"⚠ Skipped {src}: {str(e)}")
                skipped += 1
                continue

            if h in seen:
                print(f"🗑 duplicate → {src}")
                if not dry_run:
                    try:
                        os.remove(src)
                    except (PermissionError, OSError) as e:
                        print(f"⚠ Could not delete duplicate {src}: {str(e)}")
                continue
            seen[h] = src

            if os.path.dirname(src) == dest_dir:
                continue

            print(f"📁 {src} → {cat}")

            if not dry_run:
                try:
                    new_path = safe_move(src, dest_dir)
                    log.append({"from": src, "to": new_path})
                except (FileNotFoundError, PermissionError, OSError) as e:
                    print(f"⚠ Could not move {src}: {str(e)}")
                    skipped += 1
                    continue

    if not dry_run and log:
        try:
            with open(os.path.join(folder, LOG_FILE), "w") as f:
                json.dump({"timestamp": datetime.now().isoformat(), "moves": log}, f, indent=2)
        except (IOError, OSError) as e:
            print(f"⚠ Warning: Could not write log file: {str(e)}")
    
    if skipped > 0:
        print(f"\n⚠ {skipped} file(s) were skipped due to errors")

