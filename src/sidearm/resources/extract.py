from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._job import Job

if TYPE_CHECKING:
    from .._client import HttpClient


class ExtractResource:
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
    ) -> Job:
        """Extract raw embedding vectors from media. Returns a Job handle.

        The job result contains:
            embeddings: list of {algorithm, vector, dimension, metric}
            media_type: detected media type
            algorithms_applied: algorithms that succeeded
            algorithms_failed: algorithms that failed
        """
        body: dict[str, Any] = {"algorithms": algorithms}
        if media_url is not None:
            body["media_url"] = media_url
        if media is not None:
            body["media"] = media
        if text is not None:
            body["text"] = text
        if mime is not None:
            body["mime"] = mime
        res = self._http.post("/api/v1/embed", json=body)
        return Job(self._http, res["job_id"])
