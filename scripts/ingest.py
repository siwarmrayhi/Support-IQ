"""Ingestion du corpus CloudDesk : chunking, embedding, indexation."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings
from supportiq.rag.chunking import chunk_document


def load_all_chunks() -> list:
    """Parcourt data/raw/ et découpe chaque document Markdown."""
    all_chunks = []
    md_files = sorted(settings.raw_data_dir.rglob("*.md"))

    print(f"{len(md_files)} documents trouvés dans {settings.raw_data_dir}")

    for path in md_files:
        chunks = chunk_document(path)
        print(f"  {path.name:45s} -> {len(chunks)} chunk(s)")
        all_chunks.extend(chunks)

    return all_chunks


def build_index(chunks: list) -> None:
    """Encode les chunks et les stocke dans ChromaDB."""
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": True},
    )

    settings.index_dir.mkdir(parents=True, exist_ok=True)
    #cree un index a partir du doc
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(settings.index_dir),
        collection_name="supportiq",
    )


if __name__ == "__main__":
    chunks = load_all_chunks()
    print(f"\nTotal : {len(chunks)} chunks à indexer")

    build_index(chunks)
    print(f"Index créé dans {settings.index_dir}")