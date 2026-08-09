import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag import vector_store

def show_vector_db_info():
    print("=" * 60)
    print("       VECTOR DATABASE INFORMATION")
    print("=" * 60)
    
    if not vector_store.documents:
        print("\n⚠ Vector database is empty.")
        print("Please upload documents through the React app first, then run this script again.")
        return

    num_points = len(vector_store.documents)
    dimensions = vector_store.dimension
    metric = "L2 (Euclidean Distance)"
    
    # Get sources
    sources = set()
    for doc in vector_store.documents:
        sources.add(doc.get("source", "Unknown"))
    
    print(f"\n📊 Collection Name:     evidence_store")
    print(f"🟢 Status:              GREEN")
    print(f"📌 Approximate Points:  {num_points}")
    print(f"📏 Vector Dimensions:   {dimensions}")
    print(f"📐 Similarity Metric:   {metric}")
    print(f"📄 Document Sources:    {len(sources)}")
    
    print(f"\n--- Documents Indexed ---")
    for i, source in enumerate(sources, 1):
        chunks = sum(1 for doc in vector_store.documents if doc.get("source") == source)
        print(f"  {i}. {source} ({chunks} chunks)")
    
    print(f"\n--- Sample Embedding (First 10 values) ---")
    if num_points > 0:
        sample_embedding = vector_store.index.reconstruct(0)
        print(f"  Text: \"{vector_store.documents[0].get('text', '')[:80]}...\"")
        print(f"  Vector (first 10): {sample_embedding[:10].tolist()}")
    
    print(f"\n{'=' * 60}")
    print(f"Total embeddings stored: {num_points}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    show_vector_db_info()