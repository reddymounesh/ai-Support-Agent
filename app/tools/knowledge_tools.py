from app.rag.vector_store import search


async def search_knowledge_base(query: str) -> dict:
    """
    Search company policy documents for information relevant to the query.
    Returns the top matching chunks with their source document, so the
    LLM can answer using real policy text and (later) cite where it came
    from.
    """
    results = search(query, top_k=3)

    if not results:
        return {"found": False, "error": "No relevant policy information found."}

    return {
        "found": True,
        "results": [
            {"source": r["source"], "text": r["text"]} for r in results
        ],
    }