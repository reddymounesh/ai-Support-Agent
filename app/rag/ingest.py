from pathlib import Path

from app.rag.chunking import chunk_text
from app.rag.vector_store import add_chunks

POLICIES_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "policies"


def ingest_all_policies() -> None:
    doc_paths = sorted(POLICIES_DIR.glob("*.md"))

    if not doc_paths:
        print(f"No documents found in {POLICIES_DIR}")
        return

    for path in doc_paths:
        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        add_chunks(chunks, source=path.name)
        print(f"Ingested {len(chunks)} chunks from {path.name}")

    print("Ingestion complete.")


if __name__ == "__main__":
    ingest_all_policies()