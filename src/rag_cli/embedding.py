"""Responsible for embeddings"""

from sentence_transformers import SentenceTransformer

from rag_cli.config import get_config

conf = get_config()
model_path = conf["embedding"]["path"]


def get_embedding_model() -> SentenceTransformer:
    """Returns the embedding model."""
    return SentenceTransformer(model_path)
