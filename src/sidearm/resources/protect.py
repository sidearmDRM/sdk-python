from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._job import Job
from .._types import ProtectionLevel

if TYPE_CHECKING:
    from .._client import HttpClient


class ProtectResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def execute(
        self,
        *,
        media_url: str | None = None,
        media: str | None = None,
        text: str | None = None,
        mime: str | None = None,
        level: ProtectionLevel | None = None,
        tags: list[str] | None = None,
        webhook_url: str | None = None,
        filename: str | None = None,
    ) -> Job:
        """Protect media with a curated preset. Returns a Job handle."""
        body: dict[str, Any] = {}
        if media_url is not None:
            body["media_url"] = media_url
        if media is not None:
            body["media"] = media
        if text is not None:
            body["text"] = text
        if mime is not None:
            body["mime"] = mime
        if level is not None:
            body["level"] = level
        if tags is not None:
            body["tags"] = tags
        if webhook_url is not None:
            body["webhook_url"] = webhook_url
        if filename is not None:
            body["filename"] = filename
        res = self._http.post("/api/v1/protect", json=body)
        return Job(self._http, res["job_id"])
