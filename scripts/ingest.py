"""Ingestion du corpus CloudDesk : chunking, embedding, indexation."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings
from supportiq.rag.chunking import chunk_document
from supportiq.rag.vector_store import COLLECTION_NAME, get_embeddings


SUPPORTED_SUFFIXES = {".md", ".pdf"}


def load_all_chunks() -> list:
    """Parcourt data/raw/ et découpe chaque document (Markdown ou PDF)."""
    all_chunks = []
    files = sorted(
        p
        for p in settings.raw_data_dir.rglob("*")
        if p.suffix.lower() in SUPPORTED_SUFFIXES
    )

    print(f"{len(files)} documents trouvés dans {settings.raw_data_dir}")

    for path in files:
        chunks = chunk_document(path)
        extraction = chunks[0].metadata.get("extraction", "natif") if chunks else "-"
        print(f"  {path.name:45s} -> {len(chunks)} chunk(s) [{extraction}]")
        all_chunks.extend(chunks)

    return all_chunks


def build_index(chunks: list) -> None:
    """Encode les chunks et les stocke dans ChromaDB."""
    settings.index_dir.mkdir(parents=True, exist_ok=True)

    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(settings.index_dir),
        collection_name=COLLECTION_NAME,
    )


if __name__ == "__main__":
    chunks = load_all_chunks()
    print(f"\nTotal : {len(chunks)} chunks à indexer")

    build_index(chunks)
    print(f"Index créé dans {settings.index_dir}")