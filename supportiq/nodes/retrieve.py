"""Node : recherche les chunks les plus proches du ticket."""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings
from supportiq.graph.state import SupportState

_store: Chroma | None = None


def _get_store() -> Chroma:
    """Charge l'index une seule fois, puis le réutilise (cache module)."""
    global _store
    if _store is None:
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": settings.embedding_device},
            encode_kwargs={"normalize_embeddings": True},
        )
        _store = Chroma(
            persist_directory=str(settings.index_dir),
            embedding_function=embeddings,
            collection_name="supportiq",
        )
    return _store


def retrieve(state: SupportState) -> dict:
    """Recherche les 4 chunks les plus proches du ticket."""
    store = _get_store()
    docs = store.similarity_search(state["ticket"], k=4)
    return {"retrieved_docs": docs}