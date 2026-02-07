import argparse, os
from .core import organize
from .restore import restore


def main():
    parser = argparse.ArgumentParser(prog="organize")
    parser.add_argument("folder", nargs="?", default=os.getcwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")

    args = parser.parse_args()

    if args.restore:
        restore(args.folder)
    else:
        organize(args.folder, dry_run=args.dry_run)
