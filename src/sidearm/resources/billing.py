from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from .._types import BillingResponse

if TYPE_CHECKING:
    from .._client import HttpClient


class BillingResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(
        self,
        account_id: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        type: str | None = None,
        tags: str | None = None,
        token_id: str | None = None,
    ) -> BillingResponse:
        """Get billing summary, storage stats, algorithm breakdown, and events for an account."""
        return self._http.get(
            f"/api/v1/billing/{quote(account_id, safe='')}",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "type": type,
                "tags": tags,
                "token_id": token_id,
            },
        )
