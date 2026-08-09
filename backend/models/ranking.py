from dataclasses import dataclass

@dataclass
class RankingWeights:
    quality: float = 0.5
    lead_time: float = 0.3
    moq: float = 0.2

def validate_weights(weights: RankingWeights):
    total = weights.quality + weights.lead_time + weights.moq
    if abs(total - 1.0) > 0.001:
        raise ValueError("Ranking weights must add up to 1.0")