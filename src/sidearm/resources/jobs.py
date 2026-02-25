from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from .._job import Job
from .._types import JobData

if TYPE_CHECKING:
    from .._client import HttpClient


class JobsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, job_id: str) -> JobData:
        """Get the current state of a job."""
        return self._http.get(f"/api/v1/jobs/{quote(job_id, safe='')}")

    def handle(self, job_id: str) -> Job:
        """Create a Job handle for polling a previously created job."""
        return Job(self._http, job_id)
