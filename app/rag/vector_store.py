import chromadb 

from app.rag.embeddings import embed_text, embed_texts

# Persisted to disk so we don't have to re-embed documents every time the
# app restarts — the embeddings survive across runs.
_client = chromadb.PersistentClient(path="./chroma_data")

_collection = _client.get_or_create_collection(name="company_policies")


def add_chunks(chunks: list[str], source: str) -> None:
    """
    Embed and store a list of text chunks, tagging each with its source
    document (e.g. "refund_policy.md") for traceability/citations later.
    """
    embeddings = embed_texts(chunks)
    ids = [f"{source}-{i}" for i in range(len(chunks))]
    metadatas = [{"source": source} for _ in chunks]

    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )


def search(query: str, top_k: int = 3) -> list[dict]:
    """
    Embed the query and return the top_k most similar stored chunks.
    """
    query_embedding = embed_text(query)

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    matches = []
    for i in range(len(results["documents"][0])):
        matches.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i],
            }
        )
    return matches