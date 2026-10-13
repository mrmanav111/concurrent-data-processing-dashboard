from pathlib import Path

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QProgressBar, QFileDialog, QMessageBox, QGroupBox,
)

from app.data_processor import load_records, format_summary
from app.shared_state import SharedState
from app.worker import ProcessingWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Concurrent Data Processing Dashboard")
        self.resize(760, 500)

        self.data_folder: Path | None = None
        self.records: list[dict] = []
        self.shared_state = SharedState()
        self.thread: QThread | None = None
        self.worker: ProcessingWorker | None = None

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        """Create all widgets and arrange them using layouts."""
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Section 1: data folder
        data_group = QGroupBox("Data")
        data_layout = QHBoxLayout(data_group)
        self.folder_label = QLabel("No data folder selected.")
        self.load_button = QPushButton("Load Data Folder")
        self.load_button.setToolTip("Choose the folder that contains the CSV files")
        data_layout.addWidget(self.folder_label, stretch=1)
        data_layout.addWidget(self.load_button)
        main_layout.addWidget(data_group)

        # Section 2: processing controls and progress
        process_group = QGroupBox("Processing")
        process_layout = QVBoxLayout(process_group)

        button_row = QHBoxLayout()
        self.start_button = QPushButton("Start Processing")
        self.start_button.setToolTip("Calculate the totals for each category")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setToolTip("Stop the processing that is running")
        self.cancel_button.setEnabled(False)
        self.clear_button = QPushButton("Clear")
        self.clear_button.setToolTip("Clear the results and reset the progress bar")
        for button in (self.start_button, self.cancel_button, self.clear_button):
            button_row.addWidget(button)
        button_row.addStretch()
        process_layout.addLayout(button_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        process_layout.addWidget(self.progress_bar)
        main_layout.addWidget(process_group)

        # Section 3: results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        self.result_box.setPlaceholderText("Processing results will appear here...")
        results_layout.addWidget(self.result_box)
        main_layout.addWidget(results_group, stretch=1)

        # Status messages at the bottom of the window
        self.status_label = QLabel("Ready.")
        self.statusBar().addWidget(self.status_label)

    def _connect_signals(self):
        self.load_button.clicked.connect(self.choose_data_folder)
        self.start_button.clicked.connect(self.start_processing)
        self.clear_button.clicked.connect(self.clear_results)
        self.cancel_button.clicked.connect(self.cancel_processing)

    def choose_data_folder(self):
        selected = QFileDialog.getExistingDirectory(
            self, "Select the assessment data folder", str(Path.cwd())
        )
        if not selected:
            return

        try:
            self.data_folder = Path(selected)
            self.records = load_records(self.data_folder)
            self.folder_label.setText(
                f"Loaded folder: {self.data_folder.name} ({len(self.records)} records)"
            )
            self.status_label.setText("Data loaded. Ready to process.")
        except Exception as exc:
            QMessageBox.critical(self, "Load Error", str(exc))

    def start_processing(self):
        """Check the input, then start the background worker."""
        if self.thread is not None:
            return  # a job is already running
        if not self.records:
            QMessageBox.warning(
                self, "No Data", "Load the supplied data folder before starting processing."
            )
            return

        self.result_box.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Processing in the background...")
        self._set_busy(True)

        self.thread = QThread()
        self.worker = ProcessingWorker(self.records)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_processing_finished)
        self.worker.error.connect(self.on_processing_error)
        self.worker.cancelled.connect(self.on_processing_cancelled)

        for done_signal in (self.worker.finished, self.worker.error, self.worker.cancelled):
            done_signal.connect(self.thread.quit)
        self.thread.finished.connect(self._cleanup_thread)

        self.thread.start()

    def cancel_processing(self):
        """Ask the worker to stop."""
        if self.worker is not None:
            self.worker.request_cancel()
            self.status_label.setText("Cancelling...")
            self.cancel_button.setEnabled(False)

    def on_processing_finished(self, summary: dict):
        """Runs in the GUI thread when the worker has finished."""
        self.result_box.setPlainText(format_summary(summary))
        self.shared_state.mark_completed("Processing complete")
        self.status_label.setText(
            f"Complete. Jobs finished: {self.shared_state.completed_jobs}"
        )

    def on_processing_error(self, message: str):
        """Runs in the GUI thread if the worker raised an error."""
        QMessageBox.critical(self, "Processing Error", message)
        self.status_label.setText("Processing failed.")

    def on_processing_cancelled(self):
        """Runs in the GUI thread if the user cancelled."""
        self.progress_bar.setValue(0)
        self.status_label.setText("Processing cancelled.")

    def _cleanup_thread(self):
        """Release the thread and worker once the thread has stopped."""
        self.thread.deleteLater()
        self.worker.deleteLater()
        self.thread = None
        self.worker = None
        self._set_busy(False)

    def _set_busy(self, busy: bool):
        """Enable or disable buttons depending on whether a job is running."""
        self.start_button.setEnabled(not busy)
        self.load_button.setEnabled(not busy)
        self.clear_button.setEnabled(not busy)
        self.cancel_button.setEnabled(busy)

    def clear_results(self):
        """Reset the results area, progress bar and status."""
        self.result_box.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Ready.")

    def closeEvent(self, event):
        """Stop a running job cleanly if the window is closed."""
        if self.thread is not None:
            self.worker.request_cancel()
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)