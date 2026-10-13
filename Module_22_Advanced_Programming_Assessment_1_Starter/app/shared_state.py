import threading


class SharedState:
    """
    Job counter and last message that can be used safely from more than one thread.

    A lock makes sure only one thread at a time can read or change the values,
    so updates are never lost.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._completed_jobs = 0
        self._last_message = ""

    def mark_completed(self, message: str):
        """Add one to the job counter and store the message, safely."""
        with self._lock:
            self._completed_jobs += 1
            self._last_message = message

    @property
    def completed_jobs(self) -> int:
        """Read the job counter safely."""
        with self._lock:
            return self._completed_jobs

    @property
    def last_message(self) -> str:
        """Read the last message safely."""
        with self._lock:
            return self._last_message