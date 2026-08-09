from .embeddings import model as embed_model
from .vector_store import EvidenceVectorStore

# Fix the FutureWarning by using the new method name
dimension = embed_model.get_embedding_dimension()

# Create a shared singleton instance of the vector store
vector_store = EvidenceVectorStore(dimension)