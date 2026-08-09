from decision_engine.ranking import calculate_score
from decision_engine.scenarios import SCENARIOS
from models.ranking import RankingWeights

def run_sensitivity_analysis(suppliers) -> dict:
    results = {}
    
    for scenario_name, weights in SCENARIOS.items():
        scenario_results = []
        
        for supplier in suppliers:
            score = calculate_score(supplier, weights)
            scenario_results.append({
                "supplier": supplier.name,
                "score": score
            })
            
        scenario_results.sort(key=lambda item: item["score"], reverse=True)
        
        for rank, item in enumerate(scenario_results, start=1):
            item["rank"] = rank
            
        results[scenario_name] = scenario_results
        
    return results