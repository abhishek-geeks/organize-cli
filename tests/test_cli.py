"""
Tests for CLI interface (cli.py)
Tests cover: argument parsing and CLI invocation
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from organize.cli import main


class TestCLIArguments:
    """Tests for CLI argument parsing"""

    @patch("organize.cli.organize")
    def test_cli_default_folder(self, mock_organize):
        """Default folder should be current directory"""
        with patch("sys.argv", ["organize"]):
            with patch("os.getcwd", return_value="/home/user"):
                main()
                mock_organize.assert_called_once()
                # Check that the first argument is the getcwd result
                call_args = mock_organize.call_args
                assert call_args[0][0] == "/home/user"

    @patch("organize.cli.organize")
    def test_cli_specific_folder(self, mock_organize):
        """Specific folder path should be passed to organize"""
        with patch("sys.argv", ["organize", "/path/to/folder"]):
            main()
            mock_organize.assert_called_once_with("/path/to/folder", dry_run=False)

    @patch("organize.cli.organize")
    def test_cli_dry_run_flag(self, mock_organize):
        """--dry-run flag should be passed correctly"""
        with patch("sys.argv", ["organize", "--dry-run"]):
            with patch("os.getcwd", return_value="/home/user"):
                main()
                call_args = mock_organize.call_args
                assert call_args[1]["dry_run"] is True

    @patch("organize.cli.restore")
    def test_cli_restore_flag(self, mock_restore):
        """--restore flag should call restore function"""
        with patch("sys.argv", ["organize", "--restore"]):
            with patch("os.getcwd", return_value="/home/user"):
                main()
                mock_restore.assert_called_once_with("/home/user")

    @patch("organize.cli.organize")
    def test_cli_both_folder_and_dry_run(self, mock_organize):
        """Folder path and --dry-run should work together"""
        with patch("sys.argv", ["organize", "/tmp", "--dry-run"]):
            main()
            mock_organize.assert_called_once_with("/tmp", dry_run=True)


class TestCLIIntegration:
    """Integration tests for CLI"""

    def test_cli_e2e_organize(self):
        """End-to-end test: organize actual files via CLI"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file.pdf").write_text("content")
            (tmpdir / "image.jpg").write_text("image")
            
            with patch("sys.argv", ["organize", str(tmpdir)]):
                main()
            
            # Files should be organized
            assert (tmpdir / "Documents" / "file.pdf").exists()
            assert (tmpdir / "Images" / "image.jpg").exists()

    def test_cli_e2e_dry_run(self):
        """End-to-end test: dry-run should not modify files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            (tmpdir / "file.pdf").write_text("content")
            
            with patch("sys.argv", ["organize", str(tmpdir), "--dry-run"]):
                main()
            
            # File should NOT be organized
            assert (tmpdir / "file.pdf").exists()
            assert not (tmpdir / "Documents").exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
