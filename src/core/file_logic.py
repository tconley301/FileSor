import shutil
from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import QFileDialog, QMessageBox

class FileLogic:
    def __init__(self, window):

        self.window = window
        self.folder_rules: Optional[list] = None    # Will be set by UIHandler

    def bind_folder_rules(self, folder_rules: list) -> None:
        """
        Bind FileLogic to the UI's folder_rules list.
        Both will now reference the SAME list object.
        """
        self.folder_rules = folder_rules

    @staticmethod
    def resolve_name_collision(dest_dir: Path, filename: str) -> Path:
        """
        Ensure unique filenames when moving files.
        Example: 'file.txt' -> 'file (1).txt' if the name already exists.
        """
        candidate = dest_dir / filename
        if not candidate.exists():
            return candidate

        stem = Path(filename).stem
        suffix = Path(filename).suffix
        i = 1
        while True:
            candidate = dest_dir / f"{stem} ({i}){suffix}"
            if not candidate.exists():
                return candidate
            i += 1

    def find_target_for_extension(self, ext: str):
        """Find the first folder rule that matches a given file extension."""
        if not self.folder_rules:
            return None

        ext = (ext or "").lower()
        if not ext.startswith('.'):
            ext = '.' + ext if ext else ''
        for rule in self.folder_rules:
            if ext in rule['exts']:
                return rule
        return None

    def _move_one_file(self, entry: Path) -> str:
        """Move a single file to its destination folder based on extension rules."""
        try:
            rule = self.find_target_for_extension(entry.suffix)
            if not rule:
                return "skipped"
            dest_dir = Path(rule['path'])
            dest_dir.mkdir(parents=True, exist_ok=True)
            target = FileLogic.resolve_name_collision(dest_dir, entry.name)
            shutil.move(str(entry), str(target))
            return "moved"
        except Exception as e:
            print(f"Error moving {entry}: {e}")
            return "error"

    def sort_files(self):
        """Prompt user to select a folder and sort its contents."""
        source_dir = QFileDialog.getExistingDirectory(None, "Select Source Folder to Sort")
        if not source_dir:
            return
        self.sort_files_from_directory(Path(source_dir))

    def sort_files_from_directory(self, source: Path):
        """Sort all files within a selected directory based on folder rules."""
        if not self.folder_rules:
            QMessageBox.information(None, "No Rules", "Add at least one folder with allowed extensions first.")
            return
        moved = skipped = errors = 0
        for entry in source.iterdir():
            if not entry.is_file():
                continue
            result = self._move_one_file(entry)
            if result == "moved":
                moved += 1
            elif result == "skipped":
                skipped += 1
            else:
                errors += 1

        box = QMessageBox(self.window)
        box.setWindowTitle("Sorting CompleteTEST")
        box.setText(f"Sorted: {moved}\nNo extension matched: {skipped}\nErrors: {errors}")
        box.setIcon(QMessageBox.Information)
        box.setStandardButtons(QMessageBox.Ok)
        box.exec()

    def sort_individual_files(self, files: List[Path]):
        """Sort a list of individual files dropped or manually selected by the user."""
        if not self.folder_rules:
            QMessageBox.information(self.window, "No Rules", "Add at least one folder with allowed extensions first.")
            return
        moved = skipped = errors = 0
        for f in files:
            if not f.exists() or not f.is_file():
                continue
            result = self._move_one_file(f)
            if result == "moved":
                moved += 1
            elif result == "skipped":
                skipped += 1
            else:
                errors += 1

        box = QMessageBox(self.window)
        box.setWindowTitle("Sorting Complete")
        box.setText(f"Sorted: {moved}\nNo extension matched: {skipped}\nErrors: {errors}")

        box.setOption(QMessageBox.DontUseNativeDialog, True)  # <-- force Qt dialog
        box.setIcon(QMessageBox.NoIcon)  # <-- avoid Windows "info" beep
        box.setStandardButtons(QMessageBox.Ok)

        box.exec()

