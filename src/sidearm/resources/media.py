from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from .._types import EmbedMode, Media

if TYPE_CHECKING:
    from .._client import HttpClient


class MediaResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def register(
        self,
        *,
        media_url: str | None = None,
        media: str | None = None,
        mode: EmbedMode | None = None,
        expires_at: str | None = None,
        tags: list[str] | None = None,
    ) -> Media:
        """Register and index media."""
        body: dict[str, Any] = {}
        if media_url is not None:
            body["media_url"] = media_url
        if media is not None:
            body["media"] = media
        if mode is not None:
            body["mode"] = mode
        if expires_at is not None:
            body["expires_at"] = expires_at
        if tags is not None:
            body["tags"] = tags
        return self._http.post("/api/v1/media", json=body)

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Any:
        """List media assets (paginated)."""
        return self._http.get(
            "/api/v1/media",
            params={"cursor": cursor, "limit": limit},
        )

    def get(self, media_id: str) -> Media:
        """Get a specific media asset."""
        return self._http.get(f"/api/v1/media/{quote(media_id, safe='')}")

    def update(self, media_id: str, *, original_media_url: str) -> Media:
        """Update media metadata."""
        return self._http.patch(
            f"/api/v1/media/{quote(media_id, safe='')}",
            json={"original_media_url": original_media_url},
        )

    def delete(self, media_id: str) -> dict[str, bool]:
        """Permanently delete a media asset."""
        return self._http.delete(f"/api/v1/media/{quote(media_id, safe='')}")
