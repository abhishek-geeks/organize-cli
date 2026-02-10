# Organize CLI

> Smart command-line file organizer for automatic folder cleanup.

Organize CLI is a lightweight and efficient Python tool that recursively scans a directory,
categorizes files by type, removes duplicates using SHA-256 hashing, and safely organizes
everything into structured folders — all from a single command.

---

## ✨ Features

- **Recursive file organization** - Organizes files in all subdirectories
- **Category-based sorting** - Audio, Video, Images, Documents, Code, Archives, and more
- **Duplicate detection** - Uses SHA-256 hashing to identify and remove duplicates
- **Safe file moving** - Handles conflicts with automatic renaming (e.g., `file(1).txt`)
- **Dry-run preview mode** - Preview changes without making modifications
- **Restore functionality** - Undo organization and restore original file structure
- **Simple global CLI command** - Single command for organization
- **Cross-platform support** - Works on Linux, macOS, and Windows
- **Comprehensive logging** - Tracks all file movements in `.organize_log.json`
- **Error handling** - Gracefully handles permissions, missing files, and corrupted data

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

### Development Installation

```bash
git clone https://github.com/abhishek-geeks/organize-cli.git
cd organize-cli
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

---

## 🚀 Usage

### Basic Commands

```bash
# Organize current folder:
organize

# Organize a specific directory:
organize ~/Downloads

# Preview changes without moving files (dry-run):
organize --dry-run ~/Downloads

# Restore files to original locations:
organize --restore ~/Downloads
```

### Command Options

```bash
organize [PATH] [OPTIONS]

Arguments:
  PATH              Path to the folder to organize (default: current directory)

Options:
  --dry-run         Preview changes without moving files
  --restore         Restore files using the log file
  --version         Show version information
  --help            Show help message
```

---

## 📂 File Categories

Files are organized into the following categories:

| Category | Examples |
|----------|----------|
| **Audio** | `.mp3`, `.wav`, `.aac`, `.flac`, `.m4a`, `.opus` |
| **Video** | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.webm` |
| **Images** | `.jpg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg` |
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.md`, `.epub` |
| **Spreadsheets** | `.xls`, `.xlsx`, `.csv`, `.ods` |
| **Presentations** | `.ppt`, `.pptx`, `.odp`, `.key` |
| **Code** | `.py`, `.js`, `.java`, `.html`, `.css`, `.json` |
| **Archives** | `.zip`, `.rar`, `.tar`, `.gz`, `.7z` |
| **Executables** | `.exe`, `.msi`, `.deb`, `.rpm`, `.dmg` |
| **Fonts** | `.ttf`, `.otf`, `.woff`, `.woff2` |
| **Others** | Any unknown file types |

---

## 🔧 How It Works

### Organization Process

1. **Scanning** - Recursively scans all files in the directory
2. **Hashing** - Calculates SHA-256 hash for each file to detect duplicates
3. **Categorization** - Determines file category based on extension
4. **Deduplication** - Removes duplicate files (keeps first occurrence)
5. **Moving** - Moves files to category-specific subdirectories
6. **Logging** - Creates `.organize_log.json` with move history

### Duplicate Detection

Files with identical content (same SHA-256 hash) are identified as duplicates:
- The first occurrence is kept and organized
- Subsequent duplicates are deleted
- You can restore deleted files using the log file

### Conflict Resolution

If a file with the same name exists in the destination:
- Original file: `photo.jpg`
- Conflict file: `photo.jpg` → renamed to `photo(1).jpg`
- Multiple conflicts: `photo(2).jpg`, `photo(3).jpg`, etc.

### Log File

The `.organize_log.json` file stores:
- Timestamp of organization
- List of all file movements (from → to paths)
- Used for restore functionality

Example log file:
```json
{
  "timestamp": "2026-02-10T10:30:45.123456",
  "moves": [
    {"from": "./document.pdf", "to": "./Documents/document.pdf"},
    {"from": "./song.mp3", "to": "./Audio/song.mp3"}
  ]
}
```

---

## 📋 Examples

### Example 1: Basic Organization

```bash
$ organize ~/Downloads --dry-run
📁 ~/Downloads/photo.jpg → Images
📁 ~/Downloads/budget.xlsx → Spreadsheets
📁 ~/Downloads/presentation.pptx → Presentations
🗑 duplicate → ~/Downloads/photo_copy.jpg
```

### Example 2: Organize with Subdirectories

```bash
$ organize ~/Downloads
📁 ./report.pdf → Documents
📁 ./screenshot.png → Images
📁 ./project/code.py → Code
✅ Organization complete
```

### Example 3: Restore Original Structure

```bash
$ organize ~/Downloads --restore
↩ restored → ./report.pdf
↩ restored → ./screenshot.png
✅ Restore complete. Restored: 2, Failed: 0
```

---

## ⚙️ Configuration

Currently, Organize CLI uses the default file categories. Future versions will support:
- Custom category definitions
- Exclusion patterns (e.g., ignore certain file types)
- Nested category structures
- Configuration files (`.organizerc`)

---

## 🧪 Testing

Organize CLI comes with comprehensive test coverage:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage report
pytest tests/ --cov=organize

# Generate HTML coverage report
pytest tests/ --cov=organize --cov-report=html
```

Current test coverage: **65+ tests** covering:
- Core functionality (hashing, categorization, moving)
- Edge cases (special characters, unicode, long filenames)
- Error handling (permissions, missing files)
- CLI interface and arguments
- Restore functionality

---

## 🔒 Safety Features

- **Dry-run mode** - Preview changes before making them
- **Safe file moving** - Uses atomic operations
- **Automatic renaming** - Prevents file overwrites
- **Detailed logging** - Track all changes
- **Restore functionality** - Undo organization
- **Error handling** - Graceful failure on issues
- **Permission checks** - Validates folder access

---

## 🐛 Troubleshooting

### "No permission to read file"

**Problem**: Some files couldn't be accessed due to permission restrictions

**Solution**:
```bash
# Run with elevated privileges
sudo organize ~/folder
```

### "Folder does not exist"

**Problem**: The specified folder path is invalid

**Solution**:
```bash
# Check the folder path
ls ~/Downloads

# Use absolute path
organize /home/user/Downloads
```

### "Log file is corrupted"

**Problem**: The `.organize_log.json` file cannot be read

**Solution**:
```bash
# Delete the corrupted log file
rm ~/folder/.organize_log.json

# Re-organize the folder
organize ~/folder
```

### Files not being organized

**Problem**: Some files don't have recognized extensions

**Solution**:
- These files are categorized as "Others"
- You can manually move them or extend FILE_TYPES
- Check the [Contributing Guide](CONTRIBUTING.md) to add new file types

---

## 📊 Performance

Organize CLI is optimized for performance:
- **SHA-256 hashing** - Uses efficient chunked reading (8KB blocks)
- **Minimal memory usage** - Only stores hash table in memory
- **Fast file operations** - Direct OS file moving
- **Typical speed** - 1000 files per second on modern hardware

For very large folders (100k+ files), consider:
- Running multiple times on subdirectories
- Using `--dry-run` first to preview
- Checking available disk space

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Setup instructions
- Development guidelines
- Testing requirements
- Pull request process

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with Python 3.8+
- Uses standard library only (no external dependencies!)
- Inspired by the need for clean, organized folders

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/abhishek-geeks/organize-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abhishek-geeks/organize-cli/discussions)
- **Email**: abhishekgeeks@gmail.com

---

**Last Updated**: February 2026 | **Version**: 1.0.0
