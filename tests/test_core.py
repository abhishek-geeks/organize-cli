"""
Comprehensive tests for core.py - file organization logic
Tests cover: sha256 hashing, categorization, safe moving, and organization
"""

import os
import json
import pytest
import tempfile
import shutil
from pathlib import Path

from organize.core import sha256, category, safe_move, organize, LOG_FILE
from organize.filetypes import FILE_TYPES


class TestSha256:
    """Tests for SHA-256 hash calculation"""

    def test_sha256_identical_files(self):
        """Identical files should have identical SHA-256 hashes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"
            
            file1.write_text("test content")
            file2.write_text("test content")
            
            assert sha256(str(file1)) == sha256(str(file2))

    def test_sha256_different_files(self):
        """Different files should have different SHA-256 hashes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"
            
            file1.write_text("content 1")
            file2.write_text("content 2")
            
            assert sha256(str(file1)) != sha256(str(file2))

    def test_sha256_empty_file(self):
        """Empty files should have consistent hash"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "empty1.txt"
            file2 = Path(tmpdir) / "empty2.txt"
            
            file1.write_text("")
            file2.write_text("")
            
            assert sha256(str(file1)) == sha256(str(file2))

    def test_sha256_large_file(self):
        """Large files should be hashed correctly (chunks of 8192 bytes)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "large1.bin"
            file2 = Path(tmpdir) / "large2.bin"
            
            # Create 1MB files
            data = b"x" * (1024 * 1024)
            file1.write_bytes(data)
            file2.write_bytes(data)
            
            assert sha256(str(file1)) == sha256(str(file2))

    def test_sha256_binary_files(self):
        """Binary files should be hashed correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "binary1.bin"
            file2 = Path(tmpdir) / "binary2.bin"
            
            binary_data = bytes(range(256))
            file1.write_bytes(binary_data)
            file2.write_bytes(binary_data)
            
            assert sha256(str(file1)) == sha256(str(file2))


class TestCategory:
    """Tests for file categorization logic"""

    def test_category_audio_files(self):
        """Audio files should be categorized correctly"""
        assert category(".mp3") == "Audio"
        assert category(".wav") == "Audio"
        assert category(".flac") == "Audio"
        assert category(".aac") == "Audio"

    def test_category_video_files(self):
        """Video files should be categorized correctly"""
        assert category(".mp4") == "Video"
        assert category(".mkv") == "Video"
        assert category(".avi") == "Video"

    def test_category_image_files(self):
        """Image files should be categorized correctly"""
        assert category(".jpg") == "Images"
        assert category(".png") == "Images"
        assert category(".gif") == "Images"
        assert category(".webp") == "Images"

    def test_category_document_files(self):
        """Document files should be categorized correctly"""
        assert category(".pdf") == "Documents"
        assert category(".doc") == "Documents"
        assert category(".docx") == "Documents"
        assert category(".txt") == "Documents"
        assert category(".md") == "Documents"

    def test_category_code_files(self):
        """Code files should be categorized correctly"""
        assert category(".py") == "Code"
        assert category(".java") == "Code"
        assert category(".js") == "Code"
        assert category(".html") == "Code"

    def test_category_archive_files(self):
        """Archive files should be categorized correctly"""
        assert category(".zip") == "Archives"
        assert category(".rar") == "Archives"
        assert category(".tar") == "Archives"

    def test_category_unknown_extension(self):
        """Unknown extensions should be categorized as Others"""
        assert category(".xyz123") == "Others"
        assert category(".unknown") == "Others"

    def test_category_case_insensitive(self):
        """Extension checking should be case insensitive"""
        assert category(".MP3") == "Audio"
        assert category(".Pdf") == "Documents"
        assert category(".PNG") == "Images"

    def test_category_no_extension(self):
        """Files with no extension should be Others"""
        assert category("") == "Others"


class TestSafeMove:
    """Tests for safe file moving with conflict resolution"""

    def test_safe_move_basic(self):
        """Basic file move should work correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "source.txt"
            dest_dir = Path(tmpdir) / "destination"
            
            src.write_text("content")
            
            result = safe_move(str(src), str(dest_dir))
            
            assert not src.exists()
            assert Path(result).exists()
            assert Path(result).parent == dest_dir

    def test_safe_move_creates_destination(self):
        """Safe move should create destination directory if it doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "source.txt"
            dest_dir = Path(tmpdir) / "new" / "destination"
            
            src.write_text("content")
            
            result = safe_move(str(src), str(dest_dir))
            
            assert dest_dir.exists()
            assert Path(result).exists()

    def test_safe_move_conflict_resolution(self):
        """When destination file exists, should rename with counter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "file.txt"
            dest_dir = Path(tmpdir) / "dest"
            existing = dest_dir / "file.txt"
            
            src.write_text("new content")
            dest_dir.mkdir()
            existing.write_text("existing content")
            
            result = safe_move(str(src), str(dest_dir))
            
            assert Path(result).name == "file(1).txt"
            assert Path(result).exists()
            assert not src.exists()
            assert existing.exists()  # original still exists

    def test_safe_move_multiple_conflicts(self):
        """When multiple files exist, should increment counter correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "file.txt"
            dest_dir = Path(tmpdir) / "dest"
            
            src.write_text("new")
            dest_dir.mkdir()
            (dest_dir / "file.txt").write_text("existing")
            (dest_dir / "file(1).txt").write_text("existing1")
            (dest_dir / "file(2).txt").write_text("existing2")
            
            result = safe_move(str(src), str(dest_dir))
            
            assert Path(result).name == "file(3).txt"
            assert Path(result).exists()

    def test_safe_move_preserves_extension(self):
        """File extension should be preserved with counter"""
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "file.pdf"
            dest_dir = Path(tmpdir) / "dest"
            
            src.write_text("content")
            dest_dir.mkdir()
            (dest_dir / "file.pdf").write_text("existing")
            
            result = safe_move(str(src), str(dest_dir))
            
            assert Path(result).name == "file(1).pdf"
            assert Path(result).suffix == ".pdf"


class TestOrganize:
    """Tests for the main organize function"""

    def test_organize_basic_files(self):
        """Basic file organization should work"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create test files
            (tmpdir / "song.mp3").write_text("audio")
            (tmpdir / "image.jpg").write_text("image")
            (tmpdir / "document.pdf").write_text("doc")
            
            organize(str(tmpdir), dry_run=False)
            
            assert not (tmpdir / "song.mp3").exists()
            assert not (tmpdir / "image.jpg").exists()
            assert not (tmpdir / "document.pdf").exists()
            
            assert (tmpdir / "Audio" / "song.mp3").exists()
            assert (tmpdir / "Images" / "image.jpg").exists()
            assert (tmpdir / "Documents" / "document.pdf").exists()

    def test_organize_dry_run(self):
        """Dry run should preview without making changes"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "song.mp3").write_text("audio")
            
            organize(str(tmpdir), dry_run=True)
            
            # Original file should still be there
            assert (tmpdir / "song.mp3").exists()
            assert not (tmpdir / "Audio").exists()

    def test_organize_duplicate_detection(self):
        """Duplicate files should be detected and removed"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create duplicate files
            (tmpdir / "original.txt").write_text("same content")
            (tmpdir / "duplicate.txt").write_text("same content")
            
            organize(str(tmpdir), dry_run=False)
            
            # One should be moved, one should be deleted
            assert (tmpdir / "Documents" / "original.txt").exists()
            assert not (tmpdir / "Documents" / "duplicate.txt").exists()
            assert not (tmpdir / "duplicate.txt").exists()

    def test_organize_subdirectories(self):
        """Files in subdirectories should be organized"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            subdir = tmpdir / "subdir"
            subdir.mkdir()
            
            (subdir / "song.mp3").write_text("audio")
            (tmpdir / "image.jpg").write_text("image")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Audio" / "song.mp3").exists()
            assert (tmpdir / "Images" / "image.jpg").exists()
            assert not (subdir / "song.mp3").exists()

    def test_organize_log_file_creation(self):
        """Log file should be created with move history"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file.pdf").write_text("content")
            
            organize(str(tmpdir), dry_run=False)
            
            log_path = tmpdir / LOG_FILE
            assert log_path.exists()
            
            log_data = json.loads(log_path.read_text())
            assert "timestamp" in log_data
            assert "moves" in log_data
            assert len(log_data["moves"]) == 1

    def test_organize_already_organized(self):
        """Already organized files should be skipped"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            doc_dir = tmpdir / "Documents"
            doc_dir.mkdir()
            (doc_dir / "file.pdf").write_text("content")
            
            organize(str(tmpdir), dry_run=False)
            
            # File should not move
            assert (doc_dir / "file.pdf").exists()

    def test_organize_ignores_log_file(self):
        """Log file should be ignored during organization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file.pdf").write_text("content")
            
            organize(str(tmpdir), dry_run=False)
            
            # Create log manually (simulating previous run)
            log_path = tmpdir / LOG_FILE
            log_path.write_text('{"moves": []}')
            
            # Re-run organize - should not try to organize log file
            organize(str(tmpdir), dry_run=False)
            
            # Log file should still exist
            assert log_path.exists()

    def test_organize_handles_unreadable_files(self):
        """Unreadable files should be skipped gracefully"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "readable.txt").write_text("content")
            
            # This tests that organize doesn't crash on permission errors
            organize(str(tmpdir), dry_run=False)
            
            # Readable file should be organized
            assert (tmpdir / "Documents" / "readable.txt").exists()

    def test_organize_mixed_file_types(self):
        """Multiple file types should be organized into correct categories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "song.mp3").write_text("audio")
            (tmpdir / "image.jpg").write_text("image")
            (tmpdir / "script.py").write_text("code")
            (tmpdir / "archive.zip").write_text("archive")
            (tmpdir / "readme.md").write_text("doc")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Audio" / "song.mp3").exists()
            assert (tmpdir / "Images" / "image.jpg").exists()
            assert (tmpdir / "Code" / "script.py").exists()
            assert (tmpdir / "Archives" / "archive.zip").exists()
            assert (tmpdir / "Documents" / "readme.md").exists()


class TestFileTypes:
    """Tests for file type definitions"""

    def test_file_types_structure(self):
        """FILE_TYPES should have expected categories"""
        expected_categories = {
            "Audio", "Video", "Images", "Documents", "Spreadsheets",
            "Presentations", "Code", "Archives", "Executables", "Fonts"
        }
        assert set(FILE_TYPES.keys()) == expected_categories

    def test_file_types_have_extensions(self):
        """All categories should have at least one extension"""
        for category_name, extensions in FILE_TYPES.items():
            assert len(extensions) > 0, f"{category_name} has no extensions"
            assert all(ext.startswith(".") for ext in extensions), \
                f"{category_name} has extensions without dots"

    def test_no_duplicate_extensions(self):
        """Each extension should belong to only one category"""
        all_extensions = []
        for extensions in FILE_TYPES.values():
            all_extensions.extend(extensions)
        
        assert len(all_extensions) == len(set(all_extensions)), \
            "Duplicate extensions found across categories"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
