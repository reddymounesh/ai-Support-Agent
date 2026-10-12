from sentence_transformers import SentenceTransformer

# Loaded once at module import time — loading the model is relatively slow,
# so we don't want to reload it on every function call.
# "all-MiniLM-L6-v2" is small (~80MB), fast, and good enough for this use case.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> list[float]:
    """
    Convert a single piece of text into an embedding vector.
    Returns a plain Python list of floats (Chroma expects this format).
    """
    embedding = _model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Batch version — embedding many chunks at once is much faster than
    calling embed_text() in a loop, since the model can process them
    together on the CPU/GPU.
    """
    embeddings = _model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()