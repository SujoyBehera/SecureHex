"""Concurrent Inactivity Auto-Lock Manager.

Demonstrating Syllabus:
Unit-3: Concurrent Programming Paradigm - Multithreading, Daemons & Synchronization.
Tracks user interactions (mouse/key events) and triggers a thread-safe vault lock
after a configurable inactivity duration without freezing the GUI.
"""

from __future__ import annotations

import threading
import time
from typing import Callable


class AutoLockManager:
    """Daemon thread monitoring user inactivity."""

    def __init__(self, timeout_seconds: int, lock_callback: Callable[[], None]) -> None:
        self.timeout_seconds = timeout_seconds
        self.lock_callback = lock_callback
        self._last_activity_time = time.time()
        self._is_running = threading.Event()
        self._monitor_thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def start(self) -> None:
        """Starts the background daemon monitor thread."""
        with self._lock:
            if not self._is_running.is_set():
                self._is_running.set()
                self._last_activity_time = time.time()
                self._monitor_thread = threading.Thread(
                    target=self._run_monitor,
                    name="SecureHex-AutoLock-Daemon",
                    daemon=True,
                )
                self._monitor_thread.start()

    def stop(self) -> None:
        """Stops the inactivity monitor thread."""
        with self._lock:
            self._is_running.clear()

    def record_activity(self) -> None:
        """Resets the inactivity timestamp upon detecting keyboard/mouse events."""
        with self._lock:
            self._last_activity_time = time.time()

    def get_remaining_seconds(self) -> int:
        """Returns the number of idle seconds remaining before auto-lock triggers."""
        with self._lock:
            elapsed = time.time() - self._last_activity_time
            remaining = self.timeout_seconds - elapsed
            return max(0, int(remaining))

    def _run_monitor(self) -> None:
        """Worker loop executed in the daemon thread."""
        while self._is_running.is_set():
            time.sleep(1.0)
            with self._lock:
                elapsed = time.time() - self._last_activity_time
                if elapsed >= self.timeout_seconds:
                    self._is_running.clear()
                    # Trigger the UI lock callback
                    try:
                        self.lock_callback()
                    except Exception:
                        pass
                    break
