import argparse
import os
import sys
from .core import organize
from .restore import restore


def main():
    """
    Main CLI entry point for Organize CLI.
    Handles command-line arguments and error handling.
    """
    parser = argparse.ArgumentParser(
        prog="organize",
        description="Smart command-line file organizer for automatic folder cleanup"
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=os.getcwd(),
        help="Path to the folder to organize (default: current directory)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore files to original locations using log file"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    try:
        args = parser.parse_args()

        if args.restore:
            restore(args.folder)
        else:
            organize(args.folder, dry_run=args.dry_run)
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(130)  # Standard exit code for SIGINT
    except ValueError as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"❌ Permission denied: {str(e)}", file=sys.stderr)
        sys.exit(13)  # Standard exit code for EACCES
    except (OSError, IOError) as e:
        print(f"❌ File system error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

