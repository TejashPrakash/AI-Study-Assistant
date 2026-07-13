from sentence_transformers import SentenceTransformer

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    return model.encode(chunks, convert_to_tensor=False)


def create_query_embedding(query):
    return model.encode(query, convert_to_tensor=False)