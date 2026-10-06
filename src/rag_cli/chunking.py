"""Responsible for Cleaning and Chunking."""

from collections.abc import Iterator


def chunking(document: str, chunk_size: int, overlap: int = 5) -> Iterator[list[str]]:
    """Chunks a document into smaller pieces."""
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than 0.")
    if overlap < 0:
        raise ValueError("Overlap must be a non-negative integer.")

    words = document.split()

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = words[start : start + chunk_size]

        if not chunk:
            break

        yield " ".join(chunk)
