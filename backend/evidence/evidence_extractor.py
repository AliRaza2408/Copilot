import os
import json
from dotenv import load_dotenv

load_dotenv()

class EvidenceExtractor:
    def __init__(self):
        self.llm_client = None
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and groq_key != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.llm_client = Groq(api_key=groq_key)
            except Exception:
                self.llm_client = None

    def create_semantic_evidence(self, evidence_items: list[dict], supplier_name: str = None) -> list[dict]:
        """
        Takes raw page chunks and asks the LLM to identify the specific 'section' 
        and 'field' for each piece of evidence, creating rich metadata.
        Processes only the first 10 chunks to prevent Groq API rate limits.
        """
        if not evidence_items:
            return []

        enriched_evidence = []
        
        # To prevent Groq API rate limits (429 errors), we only enrich the first 10 chunks.
        # The rest are added as raw chunks so we don't lose document context for the Vector DB.
                # To prevent Groq API rate limits and speed up processing, only enrich the first 3 chunks.
        items_to_enrich = evidence_items[:3]
        remaining_items = evidence_items[3:]

        # 1. Enrich the first 10 items using the LLM
        for i, item in enumerate(items_to_enrich):
            chunk_id = f"CHUNK_{i:03d}"
            source = item.get("source", "Unknown")
            page = item.get("page", 1)
            # Truncate text to 2000 chars to keep LLM fast and avoid token limits
            text = item.get("text", "")[:2000] 

            if not self.llm_client:
                # Fallback if LLM is completely unavailable
                enriched_evidence.append({
                    "chunk_id": chunk_id,
                    "document_id": source,
                    "supplier": supplier_name or "Unknown",
                    "section": "General",
                    "field": None,
                    "page_start": page,
                    "page_end": page,
                    "text": text
                })
                continue

            system_prompt = "You are a document analyzer. Output strictly JSON."
            user_prompt = f"""Analyze this text from a manufacturing document and identify what specific 'section' and 'field' it represents.

TEXT:
{text}

INSTRUCTIONS:
1. Identify the document section (e.g., 'Company Overview', 'Manufacturing Capability', 'MOQ', 'Certifications').
2. Identify the specific field if applicable (e.g., 'minimum_order_quantity', 'lead_time', 'iso_9001').
3. Format as JSON: {{"section": "string", "field": "string or null"}}
"""
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
                metadata = json.loads(chat_completion.choices[0].message.content)
                
                # Create the enriched Evidence Object
                enriched_evidence.append({
                    "chunk_id": chunk_id,
                    "document_id": source,
                    "supplier": supplier_name or "Unknown",
                    "section": metadata.get("section", "General"),
                    "field": metadata.get("field"),
                    "page_start": page,
                    "page_end": page,
                    "text": text
                })
            except Exception as e:
                print(f"[Semantic Chunker Error] Falling back to raw chunk: {e}")
                # Fallback to original chunk if LLM fails on a specific page
                enriched_evidence.append({
                    "chunk_id": chunk_id,
                    "document_id": source,
                    "supplier": supplier_name or "Unknown",
                    "section": "General",
                    "field": None,
                    "page_start": page,
                    "page_end": page,
                    "text": text
                })

        # 2. Append the remaining items as raw chunks (no LLM call needed)
        for i, item in enumerate(remaining_items, start=10):
            enriched_evidence.append({
                "chunk_id": f"CHUNK_{i:03d}",
                "document_id": item.get("source", "Unknown"),
                "supplier": supplier_name or "Unknown",
                "section": "General",
                "field": None,
                "page_start": item.get("page", 1),
                "page_end": item.get("page", 1),
                "text": item.get("text", "")[:2000]
            })

        print(f"[Evidence Extractor] Successfully processed {len(enriched_evidence)} chunks.")
        return enriched_evidence