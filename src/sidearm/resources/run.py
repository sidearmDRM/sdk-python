from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._job import Job

if TYPE_CHECKING:
    from .._client import HttpClient


class RunResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def execute(
        self,
        *,
        algorithms: list[str],
        media_url: str | None = None,
        media: str | None = None,
        text: str | None = None,
        mime: str | None = None,
        tags: list[str] | None = None,
        webhook_url: str | None = None,
        c2pa_wrap: bool | None = None,
        filename: str | None = None,
    ) -> Job:
        """Run named algorithms on media. Returns a Job handle."""
        body: dict[str, Any] = {"algorithms": algorithms}
        if media_url is not None:
            body["media_url"] = media_url
        if media is not None:
            body["media"] = media
        if text is not None:
            body["text"] = text
        if mime is not None:
            body["mime"] = mime
        if tags is not None:
            body["tags"] = tags
        if webhook_url is not None:
            body["webhook_url"] = webhook_url
        if c2pa_wrap is not None:
            body["c2pa_wrap"] = c2pa_wrap
        if filename is not None:
            body["filename"] = filename
        res = self._http.post("/api/v1/run", json=body)
        return Job(self._http, res["job_id"])
