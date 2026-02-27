from __future__ import annotations

from typing import Any

import httpx

DEFAULT_BASE_URL = "https://api.sdrm.io"


class SidearmError(Exception):
    """Error returned by the Sidearm API."""

    def __init__(self, message: str, status: int, body: Any = None) -> None:
        super().__init__(message)
        self.status = status
        self.body = body


class HttpClient:
    """Low-level HTTP client wrapping httpx."""

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        if not api_key:
            raise ValueError("api_key is required. Get yours at https://sdrm.io/api-keys")
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._http = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
            },
            timeout=60.0,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        cleaned = {k: v for k, v in (params or {}).items() if v is not None}
        return self._request("GET", path, params=cleaned)

    def post(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self._request("POST", path, json=json)

    def patch(self, path: str, json: dict[str, Any] | None = None) -> Any:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        resp = self._http.request(method, path, **kwargs)
        if resp.status_code >= 400:
            try:
                data = resp.json()
                msg = data.get("message") or data.get("error") or resp.text
            except Exception:
                msg = resp.text
            raise SidearmError(msg, resp.status_code, body=resp.text)
        if not resp.text:
            return None
        body = resp.json()
        if isinstance(body, dict) and "data" in body:
            return body["data"]
        return body

    def close(self) -> None:
        self._http.close()
