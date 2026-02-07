# Organize CLI

> Smart command-line file organizer for automatic folder cleanup.

Organize CLI is a lightweight and efficient Python tool that recursively scans a directory,
categorizes files by type, removes duplicates using SHA-256 hashing, and safely organizes
everything into structured folders — all from a single command.

---

## ✨ Features

- Recursive file organization
- Category-based sorting (audio, video, images, documents, code, archives, etc.)
- Duplicate detection using SHA-256 hashing
- Safe file moving with conflict-free renaming
- Dry-run preview mode (no changes made)
- Simple global CLI command
- Cross-platform support (Linux, macOS, Windows)

---

## 📦 Installation

### From PyPI (recommended)

```bash
pip install organize-cli
```

### From Source:

```bash
git clone https://github.com/abhishek-geeks/organize-cli.git
cd organize-cli
pip install .
```
## 🚀 Usage

```bash
## Organize current folder:
organize

## Organize a specific directory :
organize ~/Downloads

## Preview changes without moving files:
organize --dry-run ~/Downloads