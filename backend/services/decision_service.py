import uuid
from pathlib import Path
from document_processing.document_service import process_document, evidence_to_text
from extraction.llm_extractor import LLMExtractor
from extraction.document_classifier import classify_document
from evidence.evidence_extractor import EvidenceExtractor
from decision_engine.constraint_engine import evaluate_supplier
from decision_engine.ranking import rank_suppliers
from decision_engine.missing_data import find_missing_requirements
from services.sensitivity_service import run_sensitivity_analysis
from reliability.confidence import calculate_confidence
from reliability.conflict_handler import detect_supplier_conflicts, detect_unknown_constraints
from rag import vector_store, embed_model
from models.ranking import RankingWeights
from models.requirements import Requirement
from models.supplier import Supplier
from models.decision import DecisionResult
from models.system_issue import SystemIssue

class DecisionService:
    def __init__(self):
        self.extractor = LLMExtractor()
        self.evidence_extractor = EvidenceExtractor()

    def process_case(self, file_paths: list[str]) -> dict:
        case_id = f"CASE-{uuid.uuid4().hex[:8]}"
        all_evidence = []
        req_evidence = []
        sup_evidence = []
        issues = []
        
        # 1. Process Documents & Classify
        for file_path in file_paths:
            try:
                evidence = process_document(file_path)
                all_evidence.extend(evidence)
                
                # Check for scanned PDFs
                if any(e.get("is_scanned") for e in evidence):
                    issues.append(SystemIssue(
                        type="SCANNED_PDF_DETECTED",
                        severity="HIGH",
                        message=f"{Path(file_path).name} appears to be a scanned image. Text extraction failed. OCR fallback required.",
                        requires_review=True
                    ))
                
                combined_text = " ".join([evidence_to_text(e) for e in evidence])
                doc_type = classify_document(combined_text)
                
                if doc_type == "product_requirements":
                    req_evidence.extend(evidence)
                elif doc_type == "supplier_profile":
                    sup_evidence.extend(evidence)
                else:
                    req_evidence.extend(evidence)
                    sup_evidence.extend(evidence)
            except Exception as e:
                issues.append(SystemIssue(
                    type="DOCUMENT_PROCESSING_ERROR",
                    severity="HIGH",
                    message=f"Failed to process {Path(file_path).name}: {str(e)}",
                    requires_review=True
                ))

        # Index evidence for RAG
        if all_evidence:
            texts = [evidence_to_text(item) for item in all_evidence]
            embeddings = embed_model.encode(texts)
            vector_store.add(embeddings, all_evidence)

        # 2. Dynamic LLM Extraction (with fallback)
        try:
            extracted_reqs = self.extractor.extract_requirements(req_evidence)
            extracted_sups = self.extractor.extract_suppliers(sup_evidence)
        except Exception as e:
            issues.append(SystemIssue(
                type="LLM_EXTRACTION_FAILURE",
                severity="CRITICAL",
                message="AI extraction service failed.",
                requires_review=True
            ))
            extracted_reqs, extracted_sups = [], []

        # Convert to internal models
        requirements = [
            Requirement(
                name=req.field,
                requirement_type="numeric" if isinstance(req.required_value, (int, float)) else "text",
                operator=req.operator,
                required_value=req.required_value,
                unit=req.unit,
                mandatory=req.mandatory,
                source=req.source,
                location=f"Page {req.page}" if req.page else "Unknown",
                evidence_text=""
            ) for req in extracted_reqs
        ]

        suppliers = [
            Supplier(
                name=sup.name,
                minimum_order_quantity=sup.moq,
                lead_time_days=sup.lead_time_days,
                quality_score=sup.quality_score,
                certifications=sup.certifications,
                manufacturing_capability=sup.capability
            ) for sup in extracted_sups
        ]

        # 3. Evaluate Constraints
        evaluations = []
        missing_info = []
        for supplier in suppliers:
            if not requirements:
                evaluation = {
                    "supplier": supplier.name,
                    "eligibility": "REQUIRES_REVIEW",
                    "constraints": []
                }
                missing_info.append({
                    "requirement": "Product Requirements",
                    "source": "System",
                    "location": "N/A",
                    "message": "No product requirements were found in the uploaded documents."
                })
            else:
                evaluation = evaluate_supplier(supplier, requirements)
                missing = find_missing_requirements(requirements, supplier)
                if missing:
                    missing_info.extend(missing)
            
            evaluations.append(evaluation)

        # 4. Rank & Analyze
        balanced_weights = RankingWeights(quality=0.4, lead_time=0.3, moq=0.3)
        ranking = rank_suppliers(suppliers, evaluations, balanced_weights)
        sensitivity = run_sensitivity_analysis(suppliers)

        # 5. Reliability Layer (Cross-document checks)
        issues.extend(detect_supplier_conflicts(suppliers))
        issues.extend(detect_unknown_constraints(evaluations))
        
        confidence = calculate_confidence(evaluations, missing_info, issues)

        # 6. Recommendation
        recommendation = None
        if ranking:
            top_supplier = ranking[0]
            top_eval = next((e for e in evaluations if e["supplier"] == top_supplier["supplier"]), None)
            if top_eval and top_eval["eligibility"] == "ELIGIBLE":
                recommendation = {
                    "supplier": top_supplier["supplier"],
                    "score": top_supplier["score"],
                    "confidence": confidence,
                    "approval_required": True
                }

        return DecisionResult(
            case_id=case_id,
            status="completed",
            requirements=[req.__dict__ for req in requirements],
            suppliers=[sup.__dict__ for sup in suppliers],
            evaluations=evaluations,
            ranking=ranking,
            sensitivity_analysis=sensitivity,
            conflicts=[i.dict() for i in issues], 
            missing_information=missing_info,
            evidence=all_evidence,
            recommendation=recommendation,
            review_required=bool(issues or missing_info),
            issues=[i.dict() for i in issues]
        ).dict()