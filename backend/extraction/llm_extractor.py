import os
import json
from models.extracted_data import ExtractedRequirement, ExtractedSupplier
from extraction.grounding_validator import validate_supplier_extraction

class LLMExtractor:
    def __init__(self):
        self.llm_client = None
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and groq_key != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.llm_client = Groq(api_key=groq_key)
            except Exception:
                self.llm_client = None

    def _call_llm(self, system_prompt, user_prompt):
        if not self.llm_client:
            return None
        
        try:
            chat_completion = self.llm_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"\n[LLM EXTRACTOR ERROR] {e}\n")
            return None

    def extract_requirements(self, evidence_items: list[dict]) -> list[ExtractedRequirement]:
        system_prompt = "You are a strict manufacturing requirements extractor. Output JSON with a 'requirements' array. Do not hallucinate."
        
        evidence_text = "\n".join([f"Source: {e['source']}, Page: {e.get('page',1)}\n{e['text']}" for e in evidence_items])[:6000]
        
        user_prompt = f"""Extract all mandatory product requirements from this text.
        
{evidence_text}

Rules:
1. Only extract values that are EXPLICITLY stated in the text.
2. If a value is not found, do not include it in the array.
3. DO NOT use dummy or example values. Only use what is in the text.
4. Format: {{'requirements': [{{'field': 'string', 'operator': 'string', 'required_value': 'number or string', 'unit': 'string', 'mandatory': boolean, 'source': 'string', 'page': 'number'}}]}}
"""

        result = self._call_llm(system_prompt, user_prompt)
        if result and "requirements" in result:
            valid_reqs = []
            for req in result["requirements"]:
                try:
                    valid_reqs.append(ExtractedRequirement(**req))
                except Exception as e:
                    print(f"Skipping invalid requirement: {req}")
            return valid_reqs
        return []

    def extract_suppliers(self, evidence_items: list[dict]) -> list[ExtractedSupplier]:
        system_prompt = "You are a strict supplier profile extractor. Output JSON with a 'suppliers' array. Do not hallucinate."
        
        evidence_text = "\n".join([f"Source: {e['source']}\n{e['text']}" for e in evidence_items])[:6000]
        
        user_prompt = f"""Analyze the following supplier text and extract the supplier's profile, capabilities, and commercial terms.

TEXT:
{evidence_text}

INSTRUCTIONS:
1. Extract the REAL Company Name.
2. Look for MOQ, Lead Time, Quality Score, and Certifications.
3. NORMALIZE UNITS: If lead time is given in weeks, convert to days (e.g., 4 weeks = 28 days). If MOQ is given in cartons, convert to units if possible.
4. If a value is a number, extract it as a number. If it is text (e.g., "On request"), extract it as text.
5. Format as JSON: {{"suppliers": [{{"name": "string", "moq": "number, string or null", "lead_time_days": "number, string or null", "quality_score": "number, string or null", "certifications": ["array of strings"], "source": "string"}}]}}
"""

        result = self._call_llm(system_prompt, user_prompt)
        if result and "suppliers" in result:
            suppliers = []
            fallback_source = evidence_items[0].get("source", "Unknown") if evidence_items else "Unknown"
            evidence_text = "\n".join([(e.get("text") or "") for e in evidence_items])
            
            for sup in result["suppliers"]:
                if "source" not in sup:
                    sup["source"] = fallback_source
                try:
                    extracted = ExtractedSupplier(**sup)
                    extracted.verification_status = validate_supplier_extraction(extracted, evidence_text)
                    suppliers.append(extracted)
                except Exception as e:
                    print(f"Skipping invalid supplier data: {sup}")
            return suppliers
        return []