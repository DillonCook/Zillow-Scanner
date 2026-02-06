from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ListingCandidate:
    listing_id: str
    source: str
    lane: str  # on_market | off_market
    url: str
    county: str
    price: Optional[float]
    sqft: Optional[int]
    baths: Optional[float]
    hoa: Optional[bool]
    cdd: Optional[bool]
    address: str = ""
    raw_payload: dict = field(default_factory=dict)
    scanned_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ScoredCandidate:
    candidate: ListingCandidate
    decision: str  # PASS | MAYBE | FAIL
    score: int
    reasons: List[str]
