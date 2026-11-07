"""Construction partagee du modele d'embedding et de l'index Chroma."""

from functools import lru_cache

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings

COLLECTION_NAME = "supportiq"


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": True},
    )


@lru_cache(maxsize=1)
def get_vector_store() -> Chroma:
    return Chroma(
        persist_directory=str(settings.index_dir),
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME,
    )