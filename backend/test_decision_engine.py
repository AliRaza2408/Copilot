from models.requirements import Requirement
from models.supplier import Supplier
from models.ranking import RankingWeights
from decision_engine.constraint_engine import evaluate_supplier
from decision_engine.ranking import rank_suppliers

# 1. Define Requirements
requirements = [
    Requirement(
        name="Capability",
        requirement_type="text",
        operator="==",
        required_value="Electronic Assembly",
        unit=None,
        mandatory=True,
        source="Product_Requirements.pdf",
        location="Page 1",
        evidence_text="Requires electronic assembly capability."
    ),
    Requirement(
        name="MOQ",
        requirement_type="numeric",
        operator="<=",
        required_value=1000,
        unit="units",
        mandatory=True,
        source="Product_Requirements.pdf",
        location="Page 2",
        evidence_text="Maximum MOQ is 1000 units."
    ),
    Requirement(
        name="Lead Time",
        requirement_type="numeric",
        operator="<=",
        required_value=30,
        unit="days",
        mandatory=True,
        source="Product_Requirements.pdf",
        location="Page 2",
        evidence_text="Lead time must not exceed 30 days."
    ),
    Requirement(
        name="Certification",
        requirement_type="text",
        operator="contains",
        required_value="ISO 9001",
        unit=None,
        mandatory=True,
        source="Product_Requirements.pdf",
        location="Page 3",
        evidence_text="ISO 9001 is mandatory."
    ),
    Requirement(
        name="Quality",
        requirement_type="numeric",
        operator=">=",
        required_value=90,
        unit="%",
        mandatory=True,
        source="Product_Requirements.pdf",
        location="Page 3",
        evidence_text="Quality must be >= 90%."
    )
]

# 2. Define Suppliers
suppliers = [
    Supplier(
        name="Supplier A",
        manufacturing_capability="Electronic Assembly",
        minimum_order_quantity=500,
        lead_time_days=15,
        certifications=["ISO 9001"],
        quality_score=96
    ),
    Supplier(
        name="Supplier B",
        manufacturing_capability="Electronic Assembly",
        minimum_order_quantity=2000, # FAILS MOQ
        lead_time_days=20,
        certifications=["ISO 9001"],
        quality_score=95
    ),
    Supplier(
        name="Supplier C",
        manufacturing_capability="Plastic Injection", # FAILS CAPABILITY
        minimum_order_quantity=500,
        lead_time_days=10,
        certifications=["ISO 9001"],
        quality_score=98
    ),
    Supplier(
        name="Supplier D",
        manufacturing_capability="Electronic Assembly",
        minimum_order_quantity=500,
        lead_time_days=None, # UNKNOWN LEAD TIME
        certifications=["ISO 14001"], # FAILS CERT
        quality_score=92
    )
]

# 3. Run Engine
evaluations = [evaluate_supplier(s, requirements) for s in suppliers]
results = {
    "evaluations": evaluations,
    "rankings": rank_suppliers(suppliers, evaluations, RankingWeights(quality=0.4, lead_time=0.3, moq=0.3))
}

# 4. Print Results
for eval_result in results["evaluations"]:
    print(f"\n{'='*40}")
    print(f"SUPPLIER: {eval_result['supplier']}")
    print(f"STATUS: {eval_result['eligibility']}")
    print(f"{'='*40}")
    for constraint in eval_result['constraints']:
        symbol = "✓" if constraint['status'] == "PASS" else "?" if constraint['status'] == "UNKNOWN" else "✗"
        print(f"{symbol} {constraint['requirement_name']}: {constraint['status']}")
        print(f"  -> {constraint['explanation']}")

print(f"\n{'='*40}")
print("FINAL RANKINGS (ELIGIBLE ONLY)")
print(f"{'='*40}")
for rank in results["rankings"]:
    print(f"🥇 Rank {rank['rank']}: {rank['supplier']} (Score: {rank['score']})")