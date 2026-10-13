"""Background worker that runs the slow processing off the GUI thread."""

from PyQt6.QtCore import QObject, pyqtSignal

from app.data_processor import process_records


class ProcessingCancelled(Exception):
    """Raised inside the worker when the user presses Cancel."""


class ProcessingWorker(QObject):
    """Runs process_records() in a QThread and reports back using signals."""

    progress = pyqtSignal(int)      # percentage 0-100
    finished = pyqtSignal(dict)     # summary dictionary
    error = pyqtSignal(str)         # error message
    cancelled = pyqtSignal()        # user stopped the job

    def __init__(self, records: list[dict]):
        super().__init__()
        self.records = records
        self._cancel_requested = False

    def request_cancel(self):
        """Ask the worker to stop at the next record."""
        self._cancel_requested = True

    def _report_progress(self, percent: int):
        """Called by process_records after each record."""
        if self._cancel_requested:
            raise ProcessingCancelled()
        self.progress.emit(percent)

    def run(self):
        """Do the slow work. Never touches any widget directly."""
        try:
            summary = process_records(self.records, progress_callback=self._report_progress)
            self.finished.emit(summary)
        except ProcessingCancelled:
            self.cancelled.emit()
        except Exception as exc:
            self.error.emit(str(exc))