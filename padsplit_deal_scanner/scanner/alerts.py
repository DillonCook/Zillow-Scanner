from typing import Dict, Iterable

from scanner.models import ScoredCandidate


def send_console_alert(scored_candidates: Iterable[ScoredCandidate]) -> None:
    for scored in scored_candidates:
        c = scored.candidate
        print(
            f"[ALERT] {scored.decision} | {c.lane} | {c.listing_id} | "
            f"${(c.price or 0):,.0f} | {c.sqft} sqft | {c.baths} baths | {c.url}"
        )


def send_email_alert_stub(scored_candidates: Iterable[ScoredCandidate], alert_cfg: Dict) -> None:
    if not alert_cfg.get("enabled", False):
        return
    print("[EMAIL_STUB] Email alert sending is not implemented yet.")
    print(f"[EMAIL_STUB] Would send to: {alert_cfg.get('to', [])}")
    print(f"[EMAIL_STUB] Candidate count: {len(list(scored_candidates))}")
