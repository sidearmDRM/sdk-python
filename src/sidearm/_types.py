from __future__ import annotations

from typing import Any, Literal, TypedDict


# ---------------------------------------------------------------------------
# Enums as Literal unions
# ---------------------------------------------------------------------------

MediaType = Literal["image", "video", "audio", "gif", "text", "pdf"]
AlgorithmCategory = Literal["open", "proprietary"]
EmbeddingMetric = Literal["COSINE", "L2", "IP", "HAMMING"]
ProtectionLevel = Literal["standard", "maximum"]
SearchTier = Literal["exact", "quick", "perceptual", "compositional", "full"]
DetectTier = Literal["exact", "quick", "perceptual", "compositional", "full"]
MembershipMethod = Literal["pattern", "statistical", "combined"]
EmbedMode = Literal["register", "basic", "advanced", "radioactive"]
JobStatus = Literal["queued", "running", "completed", "failed"]


# ---------------------------------------------------------------------------
# API resources
# ---------------------------------------------------------------------------


class Algorithm(TypedDict, total=False):
    id: str
    name: str
    summary: str
    description: str
    category: AlgorithmCategory
    media_types: list[MediaType]
    technique: str
    gpu_required: bool
    version: str
    """Semantic version of this algorithm implementation (e.g., '2.0.0')."""
    paper_url: str | None
    runnable: bool
    embedding_version: str | None
    """Version of the embedding model. Only present for extractable algorithms."""
    embedding_dimension: int | None
    """Dimension of vectors produced. Only present for extractable algorithms."""
    embedding_metric: EmbeddingMetric | None
    """Similarity metric. Only present for extractable algorithms."""
    active_collection: str | None
    """Active Zilliz collection name. Format: {slug}_v{major}. Only for extractable algorithms."""
    searchable_collections: list[str] | None
    """All collection names to search (current + legacy). Only for extractable algorithms."""


class Media(TypedDict, total=False):
    id: str
    account_id: str
    media_type: MediaType
    manifest: str
    storage_url: str
    original_storage_key: str
    preset: str
    algorithms_applied: list[str]
    deletes_at: str
    tags: list[str]
    metadata: dict[str, Any]
    status: Literal["active", "processing"]
    created_at: str
    updated_at: str


class JobData(TypedDict, total=False):
    id: str
    type: str
    status: JobStatus
    preset: str | None
    progress: dict[str, int] | None
    result: dict[str, Any] | None
    error: str | None
    created_at: str
    updated_at: str


class Rights(TypedDict, total=False):
    media_id: str
    c2pa: dict[str, Any]
    schema_org: dict[str, Any]
    iptc: dict[str, Any]
    tdm: dict[str, Any]
    rsl: dict[str, Any]


class BillingEvent(TypedDict, total=False):
    id: str
    type: str
    quantity: int
    unit: str
    tag: str | None
    api_token_id: str | None
    metadata: dict[str, Any] | None
    created_at: str


class BillingSummary(TypedDict, total=False):
    credit_balance: int
    total_credits_used: int
    protection_credits: int
    storage_credits: int


class StorageStats(TypedDict, total=False):
    total_bytes: int
    file_count: int
    daily_cost: int
    weekly_cost: int
    monthly_cost: int
    rate_per_mb_per_day: float


class AlgorithmUsage(TypedDict, total=False):
    algorithm: str
    display_name: str
    operations: int
    credits: int


class BillingData(TypedDict, total=False):
    summary: BillingSummary
    storage: StorageStats | None
    by_algorithm: list[AlgorithmUsage]
    events: list[BillingEvent]
    portal_url: str | None


# ---------------------------------------------------------------------------
# Response types
# ---------------------------------------------------------------------------


class JobCreatedResponse(TypedDict):
    job_id: str
    status: JobStatus
    status_url: str


class EmbeddingResult(TypedDict, total=False):
    algorithm: str
    vector: list[float]
    dimension: int
    metric: Literal["cosine", "hamming"]


class ExtractResponse(TypedDict, total=False):
    embeddings: list[EmbeddingResult]
    media_type: MediaType
    algorithms_applied: list[str]
    algorithms_failed: list[str]


class SearchResult(TypedDict, total=False):
    media_id: str
    score: float
    tier: str
    media: Media


class SearchResponse(TypedDict, total=False):
    results: list[SearchResult]


class PaginatedResponse(TypedDict, total=False):
    data: list[Any]
    cursor: str | None
    has_more: bool


class BillingResponse(TypedDict, total=False):
    summary: BillingSummary
    storage: StorageStats | None
    by_algorithm: list[AlgorithmUsage]
    events: list[BillingEvent]
    portal_url: str | None


class ProvenanceProtectionStep(TypedDict, total=False):
    id: str
    algorithm: str
    algorithm_version: str
    applied_at: str
    duration_ms: int | None
    metadata: dict[str, Any] | None


class ProvenanceSearchMatch(TypedDict, total=False):
    search_id: str
    search_type: str
    score: float
    rank: int
    searched_at: str


class ProvenanceMedia(TypedDict, total=False):
    id: str
    type: str
    account_id: str
    tags: list[str]
    is_public: bool
    created_at: str
    updated_at: str
    expires_at: str


class ProvenanceResult(TypedDict, total=False):
    media: ProvenanceMedia
    c2pa_manifest: str | None
    protection_chain: list[ProvenanceProtectionStep]
    membership_inference: list[dict[str, Any]]
    searches_found_in: list[ProvenanceSearchMatch]


class C2paChainEntry(TypedDict, total=False):
    """One step in a C2PA provenance chain, ordered from origin to current."""
    generator: str  # e.g. "Nikon Z7II", "Adobe Photoshop/24.0", "sidearm/1.0"
    title: str | None
    actions: list[str]  # e.g. ["c2pa.captured"], ["c2pa.edited"]


class IdentifyResult(TypedDict, total=False):
    """Result of fingerprint identification and C2PA extraction."""
    media_id: str | None  # Sidearm media ID if registered, else None
    c2pa_chain: list[C2paChainEntry]
