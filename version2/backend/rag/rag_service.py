import os
import json
import re
from .retriever import EvidenceRetriever
from .prompt_builder import build_prompt
from .response_validator import validate_response
from reliability.safety_guard import sanitize_prompt

class RAGService:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm_client = None
        
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and groq_key != "your_groq_api_key_here":
            try:
                from groq import Groq
                self.llm_client = Groq(api_key=groq_key)
            except Exception:
                self.llm_client = None

    def _clean_json_string(self, text: str) -> str:
        """Removes markdown code blocks if the LLM adds them despite JSON mode."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    async def answer(self, question):
        evidence = self.retriever.retrieve(question)
        prompt = build_prompt(question, evidence)
        
        # Apply safety guard against prompt injection
        safe_prompt = sanitize_prompt(prompt)

        if self.llm_client:
            try:
                chat_completion = self.llm_client.chat.completions.create(
                    messages=[{"role": "user", "content": safe_prompt}],
                    model="llama-3.1-8b-instant",
                    temperature=0.1,
                    response_format={"type": "json_object"} # <--- FORCED JSON MODE
                )
                raw_answer = chat_completion.choices[0].message.content
                
                # Clean and parse the response
                clean_answer = self._clean_json_string(raw_answer)
                parsed_answer = json.loads(clean_answer)
                
            except Exception as e:
                print(f"RAG LLM failed: {e}")
                # Graceful fallback: return structured data even if LLM fails
                parsed_answer = {
                    "facts": ["AI explanation is temporarily unavailable."],
                    "assumptions": ["System fell back to deterministic mode due to LLM error."],
                    "recommendation": "Please rely on the structured tables above.",
                    "citations": []
                }
        else:
            parsed_answer = self._mock_response(question, evidence)

        validation = validate_response(parsed_answer.get("answer", ""), evidence)
        
        return {
            "answer": parsed_answer,
            "evidence": evidence,
            "validation": validation
        }

    def _mock_response(self, question, evidence):
        facts = [doc["text"] for doc in evidence[:2]]
        citations = [{"source": doc["source"], "page": doc.get("page", 1)} for doc in evidence[:2]]
        return {
            "facts": facts,
            "assumptions": ["LLM API not configured, using simulated response."],
            "recommendation": f"Based on retrieved evidence, here is the analysis for: {question}",
            "citations": citations
        }