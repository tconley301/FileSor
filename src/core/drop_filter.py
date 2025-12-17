from PySide6.QtCore import QObject, Signal, QEvent

class DropFilter(QObject):
    """
    A reusable event filter class that enables drag-and-drop functionality.
    It listens for QEvent.DragEnter and QEvent.Drop events and emits a
    signal containing the dropped file paths.
    """
    filesDropped = Signal(list)  # Signal that emits a list[str] of dropped file paths

    def eventFilter(self, obj, event):
        """Intercepts drag/drop events and extracts local file paths."""
        if event.type() == QEvent.DragEnter:
            mime = event.mimeData()
            if mime and mime.hasUrls():
                event.acceptProposedAction()
                return True

        elif event.type() == QEvent.Drop:
            mime = event.mimeData()
            if mime and mime.hasUrls():
                paths = [url.toLocalFile() for url in mime.urls() if url.isLocalFile()]
                if paths:
                    self.filesDropped.emit(paths)
                    event.acceptProposedAction()
                    return True
        return False