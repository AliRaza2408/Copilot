from fastapi import APIRouter
from pydantic import BaseModel
from rag.rag_service import RAGService
from rag.retriever import EvidenceRetriever
from rag import vector_store, embed_model  # <-- Import shared instances

router = APIRouter(prefix="/api/copilot")

# Use the shared instances
rag_service = RAGService(EvidenceRetriever(vector_store))

class CopilotQuestion(BaseModel):
    question: str

@router.post("/ask")
async def ask_copilot(request: CopilotQuestion):
    return await rag_service.answer(request.question)

@router.post("/ingest")
async def ingest_evidence(evidence_items: list[dict]):
    texts = [item["text"] for item in evidence_items]
    if texts:
        embeddings = embed_model.encode(texts)
        vector_store.add(embeddings, evidence_items)
    return {"status": "success", "ingested": len(texts)}