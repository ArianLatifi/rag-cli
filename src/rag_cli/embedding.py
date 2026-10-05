"""Responsible for embeddings"""

import tomllib

from sentence_transformers import SentenceTransformer

with open("conf.toml", "rb") as f:
    # Load the configuration from the TOML file
    conf = tomllib.load(f)

model_path = conf["embedding"]["path"]

embedding_model = SentenceTransformer(model_path)
