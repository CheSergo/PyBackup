import os
from datetime import datetime


class ArchiveProgressTracker:
    def __init__(self, total_files: int, archive_name: str):
        self.total_files = total_files
        self.current_file = 0
        self.archive_name = archive_name
        self.start_time = datetime.now()

    def update(self, filename: str) -> None:
        """Update the progress tracker with the current file."""
        self.current_file += 1
        self._show_progress(filename)

    def _show_progress(self, filename: str) -> None:
        """Show the current tracker in the console."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if self.current_file > 0:
            rate = self.current_file / elapsed

        remaining = max(
            0,
            (self.total_files - self.current_file)
            * (elapsed / max(1, self.current_file)),
        )

        eta = (
            str(
                datetime.fromtimestamp(datetime.now().timestamp() + remaining).strftime(
                    "%H:%M:%S"
                )
            )
            if remaining > 0
            else "00:00:00"
        )

        progress = self.current_file / self.total_files * 100

        bar_length = 40
        filled_length = int(progress * bar_length / 100)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)

        print(
            f"\rArchiving {self.archive_name}: "
            f"[{bar}] {progress:.1f}% "
            f"({self.current_file}/{self.total_files}) "
            f"{eta} remaining",
            end="",
        )

        if filename:
            print(f"\nLast file: {os.path.basename(filename)}")
