import sys
from pathlib import Path

from PySide6.QtGui import QStandardItem


class Helper:

    @staticmethod
    def resource_path(relative_path: str) -> Path:
        """
        Return an absolute path to a resource that works
        both in development and in a PyInstaller .exe.
        """
        if hasattr(sys, "_MEIPASS"):
            base = Path(sys._MEIPASS)         # when running from .exe
        else:
            # this file: src/fs_utils/app_utils.py
            # parents[2] -> src/
            base = Path(__file__).resolve().parents[2]

        return base / "src" / relative_path

    @staticmethod
    def parse_exts(text: str) -> set[str]:
        """
        Convert user input like 'jpg, PNG , .pdf' into a normalized set:
        {'.jpg', '.png', '.pdf'}
        """
        exts = set()
        for part in text.split(','):
            s = part.strip().lower()
            if not s:
                continue
            if not s.startswith('.'):
                s = '.' + s
            exts.add(s)
        return exts

    @staticmethod
    def refresh_folder_list(self):
        """Rebuild the ListView based on current folder_rules."""
        self.folder_model.clear()
        for rule in self.folder_rules:
            label = rule["name"]
            if rule["exts"]:
                label += "  [ " + ", ".join(sorted(rule["exts"])) + " ]"
            item = QStandardItem(label)
            item.setEditable(False)
            item.setToolTip(rule["path"])
            self.folder_model.appendRow(item)

