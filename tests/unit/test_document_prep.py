from rag_cli.document_prep import chunking


def test_chunking():
    document = "one two three four five six seven eight"

    result = list(chunking(document, chunk_size=4, overlap=1))

    assert result == [
        ["one", "two", "three", "four"],
        ["four", "five", "six", "seven"],
        ["seven", "eight"],
    ]


def test_chunking_overlap():
    document = "one two three four five six"

    result = list(chunking(document, chunk_size=3, overlap=1))

    assert result == [
        ["one", "two", "three"],
        ["three", "four", "five"],
        ["five", "six"],
    ]


def test_chunking_empty_document():
    result = list(chunking("", chunk_size=5))

    assert result == []
