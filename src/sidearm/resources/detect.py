from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._job import Job
from .._types import DetectTier, MembershipMethod

if TYPE_CHECKING:
    from .._client import HttpClient


class DetectResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def ai(
        self,
        *,
        media_url: str | None = None,
        media: str | None = None,
        text: str | None = None,
        mime: str | None = None,
        tags: list[str] | None = None,
    ) -> Job:
        """Detect AI-generated content. Returns a Job handle."""
        body: dict[str, Any] = {}
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
        res = self._http.post("/api/v1/detect/ai", json=body)
        return Job(self._http, res["job_id"])

    def fingerprint(
        self,
        *,
        media_url: str | None = None,
        media: str | None = None,
        tags: list[str] | None = None,
        tier: DetectTier | None = None,
    ) -> Any:
        """Synchronous fingerprint detection against your indexed library."""
        body: dict[str, Any] = {}
        if media_url is not None:
            body["media_url"] = media_url
        if media is not None:
            body["media"] = media
        if tags is not None:
            body["tags"] = tags
        if tier is not None:
            body["tier"] = tier
        return self._http.post("/api/v1/detect", json=body)

    def membership(
        self,
        *,
        content_ids: list[str],
        suspect_model: str,
        method: MembershipMethod | None = None,
        tags: list[str] | None = None,
    ) -> Job:
        """Membership inference. Returns a Job handle."""
        body: dict[str, Any] = {
            "content_ids": content_ids,
            "suspect_model": suspect_model,
        }
        if method is not None:
            body["method"] = method
        if tags is not None:
            body["tags"] = tags
        res = self._http.post("/api/v1/detect/membership", json=body)
        return Job(self._http, res["job_id"])
