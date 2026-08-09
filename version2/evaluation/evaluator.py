import sys
import os
import json
from dotenv import load_dotenv

# Load the .env file from the backend directory before importing backend modules
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))
load_dotenv(dotenv_path)

# Add backend to path so we can import the decision service
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from services.decision_service import DecisionService

def run_evaluation():
    test_case_dir = os.path.join(os.path.dirname(__file__), 'test_case_001')
    expected_path = os.path.join(test_case_dir, 'expected_results.json')
    
    with open(expected_path, 'r') as f:
        ground_truth = json.load(f)
        
    file_paths = [
        os.path.join(test_case_dir, 'product_requirements.txt'),
        os.path.join(test_case_dir, 'supplier_x.txt')
    ]
    
    print("Starting Evaluation for Case 001...\n")
    
    service = DecisionService()
    result = service.process_case(file_paths)
    
    # --- DEBUG PRINTING ---
    print("=== EXTRACTED REQUIREMENTS ===")
    for req in result.get('requirements', []):
        print(f"Name: {req.get('name')} | Op: {req.get('operator')} | Val: {req.get('required_value')} | Type: {type(req.get('required_value'))}")

    print("\n=== EXTRACTED SUPPLIERS ===")
    for sup in result.get('suppliers', []):
        print(f"Name: {sup.get('name')} | MOQ: {sup.get('minimum_order_quantity')} | LeadTime: {sup.get('lead_time_days')} | Quality: {sup.get('quality_score')} | Certs: {sup.get('certifications')}")

    print("\n=== EVALUATION DETAILS ===")
    for ev in result.get('evaluations', []):
        print(f"Supplier: {ev.get('supplier')} -> Status: {ev.get('eligibility')}")
        for con in ev.get('constraints', []):
            print(f"  - {con.get('requirement_name')}: {con.get('status')} (Req: {con.get('required_value')}, Act: {con.get('actual_value')}) -> {con.get('explanation')}")
    # --- END DEBUG PRINTING ---

    print("\n--- EVALUATION RESULTS ---")
    print(f"Case ID: {result['case_id']}")
    
    actual_eligible = [e['supplier'] for e in result['evaluations'] if e['eligibility'] == 'ELIGIBLE']
    eligibility_match = set(actual_eligible) == set(ground_truth['expected_eligible'])
    print(f"\n[1] Mandatory Constraint Satisfaction:")
    print(f"    Expected: {ground_truth['expected_eligible']}")
    print(f"    Actual:   {actual_eligible}")
    print(f"    Status:   {'PASS' if eligibility_match else 'FAIL'}")
    
    actual_top = result['recommendation']['supplier'] if result['recommendation'] else None
    ranking_match = actual_top == ground_truth['expected_top_supplier']
    print(f"\n[2] Ranking Agreement:")
    print(f"    Expected: {ground_truth['expected_top_supplier']}")
    print(f"    Actual:   {actual_top}")
    print(f"    Status:   {'PASS' if ranking_match else 'FAIL'}")

    print("\nEvaluation Complete.")

if __name__ == "__main__":
    run_evaluation()