from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .._types import SearchResponse, SearchTier

if TYPE_CHECKING:
    from .._client import HttpClient


class SearchResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def run(
        self,
        *,
        media_url: str | None = None,
        media: str | None = None,
        type: SearchTier | None = None,
        tags: list[str] | None = None,
        limit: int | None = None,
    ) -> SearchResponse:
        """Run a similarity search. Returns results immediately."""
        body: dict[str, Any] = {}
        if media_url is not None:
            body["media_url"] = media_url
        if media is not None:
            body["media"] = media
        if type is not None:
            body["type"] = type
        if tags is not None:
            body["scope"] = {"tags": tags}

        path = "/api/v1/search"
        if limit is not None:
            path = f"{path}?limit={limit}"

        return self._http.post(path, json=body)

    def list(
        self,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Any:
        """List previous searches."""
        return self._http.get(
            "/api/v1/search",
            params={"cursor": cursor, "limit": limit},
        )
