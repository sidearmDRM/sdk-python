from __future__ import annotations

from typing import TYPE_CHECKING

from .._types import Algorithm, AlgorithmCategory, MediaType

if TYPE_CHECKING:
    from .._client import HttpClient


class AlgorithmsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        category: AlgorithmCategory | None = None,
        media_type: MediaType | None = None,
    ) -> list[Algorithm]:
        """List available algorithms, optionally filtered."""
        return self._http.get(
            "/api/v1/algorithms",
            params={"category": category, "media_type": media_type},
        )
