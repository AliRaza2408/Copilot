import sys
import os
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the shared vector store
from rag import vector_store

def export_embeddings():
    if not vector_store.documents:
        print("Vector database is empty. Please upload documents through the React app first.")
        return

    # Create a readable JSON file showing the text and its embedding
    export_data = []
    
    for i, doc in enumerate(vector_store.documents):
        # Reconstruct the embedding vector for this document from the FAISS index
        # FAISS stores embeddings sequentially, so we can reconstruct them
        embedding = vector_store.index.reconstruct(i)
        
        export_data.append({
            "id": i,
            "source": doc.get("source", "Unknown"),
            "page": doc.get("page", "N/A"),
            "original_text": doc.get("text", ""),
            "embedding_vector": embedding.tolist() # This is the array of numbers!
        })

    # Save to a file
    output_file = "vector_database_export.json"
    with open(output_file, "w") as f:
        json.dump(export_data, f, indent=4)
    
    print(f"\n✅ Success! Exported {len(export_data)} embeddings to '{output_file}'.")
    print(f"You can open this file to see exactly what text was extracted and what vector was assigned to it.")

if __name__ == "__main__":
    export_embeddings()