import os
import tomllib
from typing import Annotated

import chromadb
import typer

from rag_cli.document_prep import chunking
from rag_cli.embedding import embedding_model
from rag_cli.language_model import LLM

app = typer.Typer()

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="rag")  # in memory collection

with open("conf.toml", "rb") as f:
    # Load the configuration from the TOML file
    conf = tomllib.load(f)

chunk_size = conf["chunking"]["chunk_size"]
overlap = conf["chunking"]["overlap"]
top_k = conf["retrieval"]["top_k"]


@app.callback(invoke_without_command=True)
def start(path: Annotated[str, typer.Argument()] = "."):
    if path == ".":
        path = os.getcwd()

    print(f"{path=}")

    # Filter to only regular files
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    global_id_counter = 0

    # Add a progress bar across all files
    with typer.progressbar(files, label="Processing files") as progress:
        for f in progress:
            file_path = os.path.join(path, f)

            # Skip non-text files gracefully
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
            except UnicodeDecodeError, PermissionError:
                continue

            chunks = chunking(content, chunk_size, overlap)

            for chunk in chunks:
                # Ensure chunk is string format for Chroma documents
                chunk_text = " ".join(chunk) if isinstance(chunk, list) else str(chunk)

                # Encode the text
                emb_chunk = embedding_model.encode(chunk_text)
                emb_list = emb_chunk.tolist()

                # Add to ChromaDB with globally unique IDs
                collection.add(
                    ids=[f"doc_{global_id_counter}"],
                    documents=[chunk_text],
                    embeddings=[emb_list],
                    metadatas=[{"filename": f}],
                )
                global_id_counter += 1

    print("Indexing complete!\n")

    model = LLM(
        model=conf["llm"]["model"],
        api_key=conf["llm"]["API_KEY"],
        base_url=conf["llm"]["base_url"],
        temp=conf["llm"]["temperature"],
        max_new_tokens=conf["llm"]["max_new_tokens"],
    )

    # Chat Loop:
    messages = []
    while True:

        user_message = input(">>> ")
        if user_message == "\\exit":
            break
        if not user_message.strip():
            return

        emb_prompt = embedding_model.encode(user_message)
        emb_prompt_list = emb_prompt.tolist()

        # Query using only query_embeddings when supplying manual vectors
        results = collection.query(query_embeddings=[emb_prompt_list], n_results=top_k)[
            "documents"
        ][0]
        context = "\n".join(results)

        messages.append({"role": "user", "content": model.prompt_builder(user_message)})
        out = model.generate_response(messages, context)
        full_response = ""
        for e in out:
            print(e, end="", flush=True)
            full_response += e

        messages.append({"role": "assistant", "content": full_response})
        print("\n---")


if __name__ == "__main__":
    app()
