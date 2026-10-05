"""Responsible for Cleaning and Chunking."""

from collections.abc import Iterator


def chunking(document: str, chunk_size: int, overlap: int = 5) -> Iterator[list[str]]:

    words = document.split()

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = words[start : start + chunk_size]

        if not chunk:
            break

        yield chunk
