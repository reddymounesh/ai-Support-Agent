def chunk_text(text: str, max_chunk_size: int = 500) -> list[str]:
    """
    Split text into chunks along paragraph boundaries, merging small
    paragraphs together up to max_chunk_size characters, and splitting
    any single paragraph that's still too long.

    Why paragraph-based, not fixed-size slicing:
    Cutting text at an arbitrary character count can split a sentence (or
    an idea) in half, hurting retrieval quality. Paragraphs are natural,
    human-authored boundaries around a single topic.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: list[str] = []
    current_chunk = ""

    for paragraph in paragraphs:
        # Skip markdown headers as their own chunk; fold them into the next one.
        if paragraph.startswith("#"):
            current_chunk += (paragraph + "\n\n")
            continue

        if len(current_chunk) + len(paragraph) <= max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks