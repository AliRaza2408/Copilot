import faiss
import numpy as np
import os
import json

class EvidenceVectorStore:
    def __init__(self, dimension):
        self.dimension = dimension
        self.is_qdrant = False
        
        # Try to connect to Qdrant
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import Distance, VectorParams
            self.client = QdrantClient(url="http://localhost:6333")
            # Create collection if it doesn't exist
            if not self.client.collection_exists("manufacturing_evidence"):
                self.client.create_collection(
                    collection_name="manufacturing_evidence",
                    vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
                )
            self.is_qdrant = True
            print("[Vector Store] ✅ Connected to Qdrant DB.")
        except Exception:
            print("[Vector Store] ⚠️ Qdrant not available. Falling back to in-memory FAISS.")
            self.index = faiss.IndexFlatL2(dimension)
            self.documents = []

    def add(self, embeddings, documents):
        if self.is_qdrant:
            from qdrant_client.models import PointStruct
            points = []
            for i, (emb, doc) in enumerate(zip(embeddings, documents)):
                points.append(PointStruct(
                    id=i, vector=emb.tolist(), payload=doc
                ))
            self.client.upsert(collection_name="manufacturing_evidence", points=points)
        else:
            embeddings = np.asarray(embeddings).astype("float32")
            self.index.add(embeddings)
            self.documents.extend(documents)

    def search(self, embedding, top_k=5):
        if self.is_qdrant:
            results = self.client.search(
                collection_name="manufacturing_evidence",
                query_vector=embedding.tolist(),
                limit=top_k
            )
            return [res.payload for res in results]
        else:
            embedding = np.asarray([embedding]).astype("float32")
            distances, indices = self.index.search(embedding, top_k)
            results = []
            for index in indices[0]:
                if index < len(self.documents) and index != -1:
                    results.append(self.documents[index])
            return results