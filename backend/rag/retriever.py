from .embeddings import model

class EvidenceRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, question, top_k=5):
        embedding = model.encode(question)
        
        # Fetch slightly more results (10) so we can rerank and pick top 5
        initial_results = self.vector_store.search(embedding, top_k=top_k * 2)
        
        if not initial_results:
            return []

        # Basic Reranking: Boost results that contain exact words from the question
        question_words = set(question.lower().split())
        scored_results = []
        for res in initial_results:
            text = res.get("text", "").lower()
            overlap_score = sum(1 for word in question_words if word in text)
            scored_results.append((overlap_score, res))
            
        # Sort by overlap score (descending)
        scored_results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top_k results
        return [res for score, res in scored_results[:top_k]]