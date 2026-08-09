from models.requirements import Requirement
from models.supplier import Supplier
from models.ranking import RankingWeights
from decision_engine.constraint_engine import evaluate_supplier
from decision_engine.ranking import rank_suppliers
from decision_engine.missing_data import find_missing_requirements
from decision_engine.conflict_detector import detect_conflicts
from services.sensitivity_service import run_sensitivity_analysis

# 1. Requirements
requirements = [
    Requirement("Capability", "text", "==", "Electronic Assembly", None, True, "Req.pdf", "P1", "Needs Elec Assembly"),
    Requirement("MOQ", "numeric", "<=", 1000, "units", True, "Req.pdf", "P2", "Max MOQ 1000"),
    Requirement("Lead Time", "numeric", "<=", 30, "days", True, "Req.pdf", "P2", "Max LT 30 days"),
    Requirement("Certification", "text", "contains", "ISO 9001", None, True, "Req.pdf", "P3", "ISO 9001 mandatory"),
    Requirement("Quality", "numeric", ">=", 90, "%", True, "Req.pdf", "P3", "Min Quality 90%")
]

# 2. Suppliers
suppliers = [
    Supplier(name="Supplier A", manufacturing_capability="Electronic Assembly", minimum_order_quantity=500, lead_time_days=15, certifications=["ISO 9001"], quality_score=96),
    Supplier(name="Supplier B", manufacturing_capability="Electronic Assembly", minimum_order_quantity=2000, lead_time_days=20, certifications=["ISO 9001"], quality_score=95),
    Supplier(name="Supplier C", manufacturing_capability="Electronic Assembly", minimum_order_quantity=500, lead_time_days=None, certifications=[], quality_score=98)
]

# 3. Evaluate Eligibility
evaluations = [evaluate_supplier(s, requirements) for s in suppliers]

print("\n" + "="*50)
print("STEP 1: ELIGIBILITY EVALUATION")
print("="*50)
for ev in evaluations:
    print(f"\n{ev['supplier']} -> {ev['eligibility']}")
    for c in ev['constraints']:
        symbol = "✓" if c.status == "PASS" else "?" if c.status == "UNKNOWN" else "✗"
        print(f"  {symbol} {c.requirement_name}: {c.status}")

# 4. Ranking
print("\n" + "="*50)
print("STEP 2: RANKING (BALANCED WEIGHTS)")
print("="*50)
balanced_weights = RankingWeights(quality=0.4, lead_time=0.3, moq=0.3)
rankings = rank_suppliers(suppliers, evaluations, balanced_weights)
for r in rankings:
    print(f"  Rank {r['rank']}: {r['supplier']} (Score: {r['score']})")

# 5. Missing Information
print("\n" + "="*50)
print("STEP 3: MISSING INFORMATION DETECTION")
print("="*50)
for s in suppliers:
    missing = find_missing_requirements(requirements, s)
    if missing:
        print(f"\n{ s.name } is missing:")
        for m in missing:
            print(f"  - {m['requirement']}")

# 6. Conflict Detection
print("\n" + "="*50)
print("STEP 4: CONFLICT DETECTION")
print("="*50)
mock_facts = [
    {"field": "minimum_order_quantity", "value": 500, "source": "Supplier_A.pdf"},
    {"field": "minimum_order_quantity", "value": 1000, "source": "Quotation_A.xlsx"}
]
conflicts = detect_conflicts(mock_facts)
for c in conflicts:
    print(f"\n  CONFLICT on {c.field}: Values {c.values} from {c.sources}")

# 7. Sensitivity Analysis
print("\n" + "="*50)
print("STEP 5: SENSITIVITY ANALYSIS")
print("="*50)
sensitivity = run_sensitivity_analysis(suppliers)

for scenario, ranks in sensitivity.items():
    print(f"\n  Scenario: {scenario.upper()}")
    for r in ranks:
        print(f"    {r['rank']}. {r['supplier']} (Score: {r['score']})")