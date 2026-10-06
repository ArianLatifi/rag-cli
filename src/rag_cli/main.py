import os
from typing import Annotated

import typer

from rag_cli.chunking import chunking
from rag_cli.config import get_config, save_config
from rag_cli.embedding import get_embedding_model
from rag_cli.language_model import LLM
from rag_cli.vectordb import collection

app = typer.Typer()


conf = get_config()

chunk_size = conf["chunking"]["chunk_size"]
overlap = conf["chunking"]["overlap"]
top_k = conf["retrieval"]["top_k"]


@app.command(name="chat")
def chat(path: Annotated[str, typer.Argument()] = "."):
    embedding_model = get_embedding_model()
    if path == ".":
        path = os.getcwd()

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

                # Encode the text
                emb_chunk = embedding_model.encode(chunk)
                emb_list = emb_chunk.tolist()

                # Add to ChromaDB with globally unique IDs
                collection.add(
                    ids=[f"doc_{global_id_counter}"],
                    documents=[chunk],
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


@app.command("config")
def config(
    conf_list: bool = typer.Option(
        False,
        "--list",
        help="List the current configuration.",
    ),
    llm_model: str | None = typer.Option(
        None,
        "--llm-model",
        help="Set the LLM model.",
    ),
    embedding_model: str | None = typer.Option(
        None,
        "--embedding-model",
        help="Set the embedding model.",
    ),
    top_k: int | None = typer.Option(
        None,
        "--top-k",
        help="Set the number of retrieved chunks.",
    ),
    chunk_size: int | None = typer.Option(
        None,
        "--chunk-size",
        help="Set the chunk size.",
    ),
    chunk_overlap: int | None = typer.Option(
        None,
        "--chunk-overlap",
        help="Set the chunk overlap.",
    ),
):

    config = get_config()

    if conf_list:
        output = "\n".join(f"{key}: {value}" for key, value in config.items())
        typer.echo(output)

    if llm_model is not None:
        config["llm"]["model"] = llm_model

    if embedding_model is not None:
        config["embedding"]["model"] = embedding_model

    if top_k is not None:
        config["retrieval"]["top_k"] = top_k

    if chunk_size is not None:
        config["retrieval"]["chunk_size"] = chunk_size

    if chunk_overlap is not None:
        config["retrieval"]["overlap"] = chunk_overlap

    try:
        save_config(config)

    except FileNotFoundError as e:
        typer.echo(f"Failed to save configuration: {e}")

    if not conf_list:
        typer.echo("Configuration updated successfully.")


if __name__ == "__main__":
    app()
