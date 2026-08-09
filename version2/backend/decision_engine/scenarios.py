from models.ranking import RankingWeights

SCENARIOS = {
    "balanced": RankingWeights(quality=0.4, lead_time=0.3, moq=0.3),
    "quality_focused": RankingWeights(quality=0.6, lead_time=0.2, moq=0.2),
    "speed_focused": RankingWeights(quality=0.3, lead_time=0.6, moq=0.1),
    "cost_focused": RankingWeights(quality=0.2, lead_time=0.2, moq=0.6)
}