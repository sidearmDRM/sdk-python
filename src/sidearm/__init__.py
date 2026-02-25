"""Sidearm Python SDK."""

from __future__ import annotations

from ._client import HttpClient, SidearmError
from ._job import Job
from .resources.algorithms import AlgorithmsResource
from .resources.billing import BillingResource
from .resources.detect import DetectResource
from .resources.jobs import JobsResource
from .resources.media import MediaResource
from .resources.protect import ProtectResource
from .resources.rights import RightsResource
from .resources.run import RunResource
from .resources.search import SearchResource


class Sidearm:
    """Sidearm API client.

    Usage::

        from sidearm import Sidearm

        client = Sidearm(api_key="sk_live_...")
        job = client.protect(media_url="https://...", level="maximum")
        result = job.wait()
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str | None = None,
    ) -> None:
        self._http = HttpClient(api_key, base_url)
        self._run = RunResource(self._http)
        self._protect = ProtectResource(self._http)

        self.algorithms = AlgorithmsResource(self._http)
        """Browse and discover available algorithms."""

        self.jobs = JobsResource(self._http)
        """Poll and manage async jobs."""

        self.search = SearchResource(self._http)
        """Similarity search across your media library."""

        self.detect = DetectResource(self._http)
        """AI detection, fingerprint detection, membership inference."""

        self.media = MediaResource(self._http)
        """Register, list, update, and delete media assets."""

        self.rights = RightsResource(self._http)
        """Rights and licensing information."""

        self.billing = BillingResource(self._http)
        """Billing and usage events."""

    def run(self, **kwargs) -> Job:
        """Run named algorithms on media. Returns a Job handle."""
        return self._run.execute(**kwargs)

    def protect(self, **kwargs) -> Job:
        """Protect media with a curated preset. Returns a Job handle."""
        return self._protect.execute(**kwargs)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> Sidearm:
        return self

    def __exit__(self, *args) -> None:
        self.close()


__all__ = [
    "Sidearm",
    "SidearmError",
    "Job",
]
