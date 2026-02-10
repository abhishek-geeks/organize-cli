"""
Edge case tests for Organize CLI
Tests for: special characters, no extension, hidden files, symlinks, etc.
"""

import os
import pytest
import tempfile
from pathlib import Path

from organize.core import category, organize, LOG_FILE


class TestEdgeCases:
    """Tests for edge cases and special scenarios"""

    def test_file_with_no_extension(self):
        """Files with no extension should be categorized as Others"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "Makefile").write_text("makefile content unique 1")
            (tmpdir / "README").write_text("readme content unique 2")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Others" / "Makefile").exists()
            assert (tmpdir / "Others" / "README").exists()

    def test_file_with_multiple_dots(self):
        """Files with multiple dots should use last extension"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # archive.tar.gz should be recognized as .gz (Archives)
            (tmpdir / "backup.tar.gz").write_text("archive content unique 1")
            # image.backup.jpg should be recognized as .jpg (Images)
            (tmpdir / "photo.backup.jpg").write_text("image content unique 2")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Archives" / "backup.tar.gz").exists()
            assert (tmpdir / "Images" / "photo.backup.jpg").exists()

    def test_file_with_special_characters(self):
        """Files with special characters in names should be handled"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file with spaces.txt").write_text("text content unique 1")
            (tmpdir / "file-with-dashes.pdf").write_text("pdf content unique 2")
            (tmpdir / "file_with_underscores.mp3").write_text("audio content unique 3")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "file with spaces.txt").exists()
            assert (tmpdir / "Documents" / "file-with-dashes.pdf").exists()
            assert (tmpdir / "Audio" / "file_with_underscores.mp3").exists()

    def test_file_with_unicode_characters(self):
        """Files with unicode characters should be handled"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "文件.txt").write_text("chinese content unique")
            (tmpdir / "фото.jpg").write_text("russian content unique")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "文件.txt").exists()
            assert (tmpdir / "Images" / "фото.jpg").exists()

    def test_hidden_files(self):
        """Hidden files (starting with dot) should be organized"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / ".hidden.txt").write_text("hidden text content unique")
            (tmpdir / ".config.json").write_text("config json content unique")
            
            organize(str(tmpdir), dry_run=False)
            
            # Hidden files should be categorized and moved
            assert (tmpdir / "Documents" / ".hidden.txt").exists()
            assert (tmpdir / "Code" / ".config.json").exists()

    def test_very_long_filename(self):
        """Very long filenames should be handled correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            long_name = "a" * 200 + ".pdf"
            (tmpdir / long_name).write_text("long filename pdf content unique")
            
            organize(str(tmpdir), dry_run=False)
            
            # File should be organized despite long name
            assert (tmpdir / "Documents" / long_name).exists()

    def test_file_with_uppercase_extension(self):
        """Files with uppercase extensions should be recognized"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "image.JPG").write_text("jpg image content unique 1")
            (tmpdir / "document.PDF").write_text("pdf doc content unique 2")
            (tmpdir / "audio.MP3").write_text("mp3 audio content unique 3")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Images" / "image.JPG").exists()
            assert (tmpdir / "Documents" / "document.PDF").exists()
            assert (tmpdir / "Audio" / "audio.MP3").exists()

    def test_mixed_case_extension(self):
        """Files with mixed case extensions should be recognized"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file.Pdf").write_text("mixed case pdf content unique")
            (tmpdir / "image.JpG").write_text("mixed case jpg content unique")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "file.Pdf").exists()
            assert (tmpdir / "Images" / "image.JpG").exists()

    def test_file_starting_with_dot(self):
        """Files starting with dot should not be treated as hidden when creating category dir"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / ".DS_Store").write_text("mac store file content unique")
            (tmpdir / ".gitignore").write_text("git ignore file content unique")
            
            organize(str(tmpdir), dry_run=False)
            
            # Should be organized into Others category
            assert (tmpdir / "Others" / ".DS_Store").exists()
            assert (tmpdir / "Others" / ".gitignore").exists()

    def test_empty_directory(self):
        """Empty directory should not cause issues"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "empty_dir").mkdir()
            
            # Should not raise an exception
            organize(str(tmpdir), dry_run=False)
            
            # Empty directory should remain
            assert (tmpdir / "empty_dir").exists()

    def test_deeply_nested_subdirectories(self):
        """Files in deeply nested subdirectories should be organized"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            deep_dir = tmpdir / "a" / "b" / "c" / "d"
            deep_dir.mkdir(parents=True)
            (deep_dir / "file.pdf").write_text("deep nested content unique")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "file.pdf").exists()

    def test_file_conflicts_in_same_operation(self):
        """Multiple files with same name should be numbered correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file.txt").write_text("content1 unique")
            (tmpdir / "subdir1").mkdir()
            (tmpdir / "subdir1" / "file.txt").write_text("content2 unique")
            (tmpdir / "subdir2").mkdir()
            (tmpdir / "subdir2" / "file.txt").write_text("content3 unique")
            
            organize(str(tmpdir), dry_run=False)
            
            # All three should be in Documents with different names
            assert (tmpdir / "Documents" / "file.txt").exists()
            assert (tmpdir / "Documents" / "file(1).txt").exists()
            assert (tmpdir / "Documents" / "file(2).txt").exists()

    def test_category_only_lowercase_extensions(self):
        """Category function should accept only lowercase input after fix"""
        # After our fix, the category function handles both cases
        assert category(".pdf") == "Documents"
        assert category(".PDF") == "Documents"
        assert category(".Pdf") == "Documents"

    def test_organize_handles_numeric_filenames(self):
        """Numeric filenames should be handled"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "123.pdf").write_text("numeric pdf file unique 1")
            (tmpdir / "456.mp3").write_text("numeric mp3 file unique 2")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "123.pdf").exists()
            assert (tmpdir / "Audio" / "456.mp3").exists()

    def test_organize_handles_parentheses_in_names(self):
        """Filenames with parentheses should work correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file (1).txt").write_text("parentheses txt file unique")
            (tmpdir / "video (2).mp4").write_text("parentheses video file unique")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "file (1).txt").exists()
            assert (tmpdir / "Video" / "video (2).mp4").exists()

    def test_file_with_spaces_at_edges(self):
        """Files with spaces at name edges should be handled"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Note: filesystem might not allow spaces at edges
            # but testing with internal spaces
            (tmpdir / "my file.txt").write_text("spaced text file unique")
            
            organize(str(tmpdir), dry_run=False)
            
            assert (tmpdir / "Documents" / "my file.txt").exists()


class TestCategoryEdgeCases:
    """Edge case tests for category function"""

    def test_category_tar_gz(self):
        """.tar.gz should be recognized as archive"""
        # Testing with the last extension
        assert category(".gz") == "Archives"

    def test_category_empty_string(self):
        """Empty extension should return Others"""
        assert category("") == "Others"

    def test_category_dot_only(self):
        """Just a dot should return Others"""
        assert category(".") == "Others"

    def test_category_all_supported_formats(self):
        """All documented formats should be recognized"""
        test_cases = {
            ".mp3": "Audio",
            ".mp4": "Video",
            ".jpg": "Images",
            ".pdf": "Documents",
            ".xls": "Spreadsheets",
            ".ppt": "Presentations",
            ".py": "Code",
            ".zip": "Archives",
            ".exe": "Executables",
            ".ttf": "Fonts",
        }
        for ext, expected_cat in test_cases.items():
            assert category(ext) == expected_cat, f"{ext} should be {expected_cat}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
