"""
Tests for restore functionality (restore.py)
Tests cover: restoring files to original locations
"""

import json
import pytest
import tempfile
from pathlib import Path

from organize.restore import restore
from organize.core import LOG_FILE


class TestRestore:
    """Tests for restore functionality"""

    def test_restore_basic(self):
        """Basic file restoration should work"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Create log file with move history
            log_data = {
                "timestamp": "2026-02-10T10:00:00",
                "moves": [
                    {
                        "from": str(tmpdir / "file.pdf"),
                        "to": str(tmpdir / "Documents" / "file.pdf")
                    }
                ]
            }
            
            (tmpdir / LOG_FILE).write_text(json.dumps(log_data))
            
            # Create the file in its moved location
            (tmpdir / "Documents").mkdir()
            (tmpdir / "Documents" / "file.pdf").write_text("content")
            
            restore(str(tmpdir))
            
            # File should be restored to original location
            assert (tmpdir / "file.pdf").exists()
            assert not (tmpdir / "Documents" / "file.pdf").exists()

    def test_restore_multiple_files(self):
        """Multiple files should be restored in reverse order"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            log_data = {
                "timestamp": "2026-02-10T10:00:00",
                "moves": [
                    {
                        "from": str(tmpdir / "file1.txt"),
                        "to": str(tmpdir / "Documents" / "file1.txt")
                    },
                    {
                        "from": str(tmpdir / "file2.jpg"),
                        "to": str(tmpdir / "Images" / "file2.jpg")
                    }
                ]
            }
            
            (tmpdir / LOG_FILE).write_text(json.dumps(log_data))
            
            # Create moved files
            (tmpdir / "Documents").mkdir()
            (tmpdir / "Images").mkdir()
            (tmpdir / "Documents" / "file1.txt").write_text("text")
            (tmpdir / "Images" / "file2.jpg").write_text("image")
            
            restore(str(tmpdir))
            
            # Both files should be restored
            assert (tmpdir / "file1.txt").exists()
            assert (tmpdir / "file2.jpg").exists()
            assert not (tmpdir / "Documents" / "file1.txt").exists()
            assert not (tmpdir / "Images" / "file2.jpg").exists()

    def test_restore_no_log_file(self):
        """Restore without log file should handle gracefully"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Should not raise an exception
            restore(tmpdir)

    def test_restore_missing_file(self):
        """Restore should handle files that no longer exist at the moved location"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            log_data = {
                "timestamp": "2026-02-10T10:00:00",
                "moves": [
                    {
                        "from": str(tmpdir / "file.pdf"),
                        "to": str(tmpdir / "Documents" / "file.pdf")
                    }
                ]
            }
            
            (tmpdir / LOG_FILE).write_text(json.dumps(log_data))
            
            # File doesn't exist at moved location
            # Should not raise an exception
            restore(str(tmpdir))
            
            # Original location should not have the file
            assert not (tmpdir / "file.pdf").exists()

    def test_restore_creates_original_directory(self):
        """Restore should create original directory if it doesn't exist"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            log_data = {
                "timestamp": "2026-02-10T10:00:00",
                "moves": [
                    {
                        "from": str(tmpdir / "subdir" / "file.txt"),
                        "to": str(tmpdir / "Documents" / "file.txt")
                    }
                ]
            }
            
            (tmpdir / LOG_FILE).write_text(json.dumps(log_data))
            
            (tmpdir / "Documents").mkdir()
            (tmpdir / "Documents" / "file.txt").write_text("content")
            
            restore(str(tmpdir))
            
            # Original directory should be created
            assert (tmpdir / "subdir").exists()
            assert (tmpdir / "subdir" / "file.txt").exists()

    def test_restore_empty_log(self):
        """Restore with empty moves list should work"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            log_data = {
                "timestamp": "2026-02-10T10:00:00",
                "moves": []
            }
            
            (tmpdir / LOG_FILE).write_text(json.dumps(log_data))
            
            # Should not raise an exception
            restore(str(tmpdir))

    def test_restore_preserves_file_content(self):
        """Restored files should maintain their original content"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            original_content = "Important data"
            
            log_data = {
                "timestamp": "2026-02-10T10:00:00",
                "moves": [
                    {
                        "from": str(tmpdir / "file.txt"),
                        "to": str(tmpdir / "Documents" / "file.txt")
                    }
                ]
            }
            
            (tmpdir / LOG_FILE).write_text(json.dumps(log_data))
            
            (tmpdir / "Documents").mkdir()
            (tmpdir / "Documents" / "file.txt").write_text(original_content)
            
            restore(str(tmpdir))
            
            # Content should be preserved
            assert (tmpdir / "file.txt").read_text() == original_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
