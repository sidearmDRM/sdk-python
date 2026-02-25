# sidearmdrm

Python SDK for the [Sidearm API](https://sdrm.io). Protect media from AI training, detect AI content, search for stolen work.

## Install

```bash
pip install sidearmdrm
```

## Quick Start

```python
from sidearm import Sidearm

client = Sidearm(api_key="sk_live_...")
job = client.protect(media_url="https://example.com/art.png", level="maximum")
result = job.wait()
print(result)
```

## Protection

```python
# Preset level (auto-selects algorithms)
job = client.protect(media_url="https://...", level="standard", tags=["portfolio"])

# Run specific algorithms by name
job = client.run(algorithms=["nightshade", "glaze", "hmark"], media_url="https://...")
```

## Job Polling

Async endpoints return a Job handle with built-in polling:

```python
# Wait until done (default 120s timeout, 2s interval)
result = job.wait(timeout=120, interval=2)

# Manual poll
status = job.poll()

# Resume from a previous job ID
resumed = client.jobs.handle("job-uuid")
resumed.wait()
```

## Algorithms

```python
all_algos = client.algorithms.list()
audio = client.algorithms.list(media_type="audio")
open_algos = client.algorithms.list(category="open")
```

## Detection

```python
# AI content detection (async)
ai_job = client.detect.ai(media_url="https://...")
ai_result = ai_job.wait()

# Fingerprint detection (sync)
matches = client.detect.fingerprint(media_url="https://...", tier="perceptual")

# Membership inference
mem_job = client.detect.membership(
    content_ids=["uuid-1", "uuid-2"],
    suspect_model="stable-diffusion-xl",
    method="combined",
)
mem_result = mem_job.wait()
```

## Search

```python
results = client.search.run(media_url="https://...", type="perceptual", limit=10)
history = client.search.list(limit=20)
```

## Media Management

```python
media = client.media.register(media_url="https://...", mode="basic")
library = client.media.list(limit=50)
asset = client.media.get("uuid")
client.media.update("uuid", original_media_url="https://...")
client.media.delete("uuid")
```

## Rights and Billing

```python
rights = client.rights.get("media-uuid")
billing = client.billing.get("account-uuid", start_date="2026-01-01")
```

## Error Handling

```python
from sidearm import Sidearm, SidearmError

try:
    client.protect(media_url="...")
except SidearmError as e:
    print(e)          # Human-readable message
    print(e.status)   # HTTP status code
    print(e.body)     # Raw response body
```

## Context Manager

```python
with Sidearm(api_key="sk_live_...") as client:
    job = client.protect(media_url="https://...")
    result = job.wait()
```

## Requirements

- Python 3.9+
- Single dependency: httpx
- Full type annotations (py.typed)

## License

MIT
