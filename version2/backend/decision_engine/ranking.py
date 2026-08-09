from models.supplier import Supplier
from models.ranking import RankingWeights

def safe_float(val):
    """Safely convert LLM outputs to floats for comparison."""
    if val is None:
        return None
    try:
        # Remove common text like '%', 'days', 'units' if the LLM included them
        cleaned = str(val).replace('%', '').replace('days', '').replace('units', '').replace(',', '').strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return None

def calculate_score(supplier: Supplier, weights: RankingWeights) -> float:
    score = 0.0

    # Use safe_float for all math operations
    if supplier.quality_score is not None:
        quality_val = safe_float(supplier.quality_score)
        if quality_val is not None:
            quality_score = min(quality_val, 100)
            score += quality_score * weights.quality

    if supplier.lead_time_days is not None:
        lead_time_val = safe_float(supplier.lead_time_days)
        if lead_time_val is not None:
            lead_time_score = max(0, 100 - lead_time_val)
            score += lead_time_score * weights.lead_time

    if supplier.minimum_order_quantity is not None:
        moq_val = safe_float(supplier.minimum_order_quantity)
        if moq_val is not None:
            moq_score = max(0, 100 - (moq_val / 100))
            score += moq_score * weights.moq

    return round(score, 2)

def rank_suppliers(suppliers: list[Supplier], evaluations: list[dict], weights: RankingWeights) -> list[dict]:
    eligible = []

    if not suppliers or not evaluations:
        return []

    for supplier, evaluation in zip(suppliers, evaluations):
        if evaluation and evaluation.get("eligibility") == "ELIGIBLE":
            score = calculate_score(supplier, weights)
            eligible.append({
                "supplier": supplier.name,
                "score": score
            })

    eligible.sort(key=lambda item: item["score"], reverse=True)

    for index, item in enumerate(eligible, start=1):
        item["rank"] = index

    return eligible