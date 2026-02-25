from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from .._types import Rights

if TYPE_CHECKING:
    from .._client import HttpClient


class RightsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self, media_id: str) -> Rights:
        """Get C2PA, IPTC, and licensing information for a media asset."""
        return self._http.get(f"/api/v1/rights/{quote(media_id, safe='')}")
