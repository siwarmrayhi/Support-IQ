"""Interroge l'index Chroma et affiche les résultats avec leurs scores."""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from supportiq.config import settings


def load_vector_store() -> Chroma:
    """Recharge l'index existant depuis le disque."""
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": settings.embedding_device},
        encode_kwargs={"normalize_embeddings": True},
    )
    #ouvre un index déja existant sur le disque à l'endroit indiqué par persist_directory
    return Chroma(
        persist_directory=str(settings.index_dir),
        embedding_function=embeddings,
        collection_name="supportiq",
    )


def search(query: str, k: int = 4) -> None:
    """Affiche les k chunks les plus proches d'une requête."""
    store = load_vector_store()
    results = store.similarity_search_with_score(query, k=k)

    print(f"\nRequête : {query!r}")
    print(f"{len(results)} résultat(s)\n")

    for rank, (doc, distance) in enumerate(results, start=1):
        print(f"--- #{rank}  distance={distance:.4f} ---")
        print(f"doc_id : {doc.metadata.get('doc_id')}")
        print(f"titre  : {doc.metadata.get('title')}")
        print(doc.page_content[:200].replace("\n", " "))
        print()


if __name__ == "__main__":
    search("DC-4092")