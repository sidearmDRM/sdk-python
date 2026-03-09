from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from .._types import SharedResult

if TYPE_CHECKING:
    from .._client import HttpClient


class SharesResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, type: str, result_id: str) -> SharedResult:
        """Create a shareable link for a result."""
        return self._http.post(
            "/api/v1/shares",
            json={"type": type, "result_id": result_id},
        )

    def get(self, share_id: str) -> SharedResult:
        """Get a shared result by ID."""
        return self._http.get(f"/api/v1/shares/{quote(share_id, safe='')}")

    def publish(self, share_id: str) -> SharedResult:
        """Make a shared result publicly accessible."""
        return self._http.patch(
            f"/api/v1/shares/{quote(share_id, safe='')}",
            json={"is_public": True},
        )
