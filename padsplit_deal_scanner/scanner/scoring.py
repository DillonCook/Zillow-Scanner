from typing import Dict, List

from scanner.models import ListingCandidate, ScoredCandidate


def score_candidate(candidate: ListingCandidate, cfg: Dict) -> ScoredCandidate:
    reasons: List[str] = []
    score = 0

    if candidate.county not in cfg.get("counties", []):
        reasons.append(f"County {candidate.county} not in target counties")
        return ScoredCandidate(candidate=candidate, decision="FAIL", score=0, reasons=reasons)

    if candidate.price is not None and candidate.price <= cfg["max_on_market_price"]:
        score += 2
        reasons.append(f"Price ${candidate.price:,.0f} <= ${cfg['max_on_market_price']:,.0f}")
    else:
        reasons.append(
            f"Price too high or missing (got {candidate.price}, max {cfg['max_on_market_price']})"
        )

    if candidate.sqft is not None:
        if candidate.sqft >= cfg["min_sqft_strong"]:
            score += 2
            reasons.append(f"Strong sqft: {candidate.sqft} >= {cfg['min_sqft_strong']}")
        elif candidate.sqft >= cfg["min_sqft_soft"]:
            score += 1
            reasons.append(f"Soft sqft: {candidate.sqft} >= {cfg['min_sqft_soft']}")
        else:
            reasons.append(f"Sqft below soft threshold: {candidate.sqft}")
    else:
        reasons.append("Sqft missing")

    if candidate.baths is not None:
        if candidate.baths >= cfg["min_baths_strong"]:
            score += 2
            reasons.append(f"Strong baths: {candidate.baths} >= {cfg['min_baths_strong']}")
        elif candidate.baths >= cfg["min_baths_soft"]:
            score += 1
            reasons.append(f"Soft baths: {candidate.baths} >= {cfg['min_baths_soft']}")
        else:
            reasons.append(f"Baths below soft threshold: {candidate.baths}")
    else:
        reasons.append("Bath count missing")

    if candidate.hoa is True and cfg.get("hoa_policy") == "reject_if_yes":
        reasons.append("HOA present and policy is reject_if_yes")
        return ScoredCandidate(candidate=candidate, decision="FAIL", score=score, reasons=reasons)

    if candidate.cdd is True and cfg.get("cdd_policy") == "warn_if_yes":
        reasons.append("CDD present; policy warns")

    if score >= 6:
        decision = "PASS"
    elif score >= 3:
        decision = "MAYBE"
    else:
        decision = "FAIL"

    return ScoredCandidate(candidate=candidate, decision=decision, score=score, reasons=reasons)
