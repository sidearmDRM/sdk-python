from __future__ import annotations

import time
from typing import TYPE_CHECKING
from urllib.parse import quote

from ._types import JobData

if TYPE_CHECKING:
    from ._client import HttpClient

_DEFAULT_TIMEOUT = 120.0
_DEFAULT_INTERVAL = 2.0


class Job:
    """Handle to an asynchronous Sidearm job with polling helpers."""

    def __init__(self, http: HttpClient, job_id: str) -> None:
        self._http = http
        self.id = job_id
        self._latest: JobData = {"id": job_id, "status": "queued"}

    @property
    def latest(self) -> JobData:
        """Most recently fetched job data."""
        return self._latest

    @property
    def done(self) -> bool:
        """Whether the job reached a terminal state."""
        return self._latest.get("status") in ("completed", "failed")

    def poll(self) -> JobData:
        """Fetch the current job state from the API."""
        self._latest = self._http.get(f"/api/v1/jobs/{quote(self.id, safe='')}")
        return self._latest

    def wait(
        self,
        *,
        timeout: float = _DEFAULT_TIMEOUT,
        interval: float = _DEFAULT_INTERVAL,
    ) -> JobData:
        """Poll until the job completes or fails.

        Args:
            timeout: Maximum seconds to wait (default 120).
            interval: Seconds between polls (default 2).

        Raises:
            TimeoutError: If the job does not finish within *timeout*.
        """
        deadline = time.monotonic() + timeout
        while not self.done:
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Job {self.id} did not complete within {timeout}s "
                    f"(last status: {self._latest.get('status')})"
                )
            time.sleep(interval)
            self.poll()
        return self._latest
