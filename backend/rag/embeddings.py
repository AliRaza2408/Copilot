from sentence_transformers import SentenceTransformer

# Load the model once when the module is imported
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(texts):
    return model.encode(texts, convert_to_numpy=True)