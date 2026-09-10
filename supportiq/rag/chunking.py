"""Stratégies de découpage des documents selon leur type de source."""

from pathlib import Path

import frontmatter
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Un token français fait environ 0,75 mot en moyenne avec bge-m3.
_LONG_TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=150,
    separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
)

def load_raw_document(path: Path) -> tuple[dict, str]:
    """Sépare l'en-tête YAML (metadata) du corps Markdown (content)."""
    post = frontmatter.load(path)
    return post.metadata, post.content


def chunk_faq(metadata: dict, content: str) -> list[Document]:
    """Un chunk par paire question/réponse (chaque section '## ')."""
    sections = content.split("\n## ")
    chunks = []
    for i, section in enumerate(sections):
        text = section.strip()
        if not text:
            continue
        if not text.startswith("#"):
            text = "## " + text
        chunks.append(
            Document(
                page_content=text,
                metadata={**metadata, "chunk_index": i},
            )
        )
    return chunks


def chunk_ticket(metadata: dict, content: str) -> list[Document]:
    """Un ticket historique = un seul chunk, jamais découpé."""
    return [
        Document(
            page_content=content.strip(),
            metadata={**metadata, "chunk_index": 0},
        )
    ]


def chunk_long_text(metadata: dict, content: str) -> list[Document]:
    """Découpage récursif pour la documentation et les guides."""
    fragments = _LONG_TEXT_SPLITTER.split_text(content)
    return [
        Document(
            page_content=fragment,
            metadata={**metadata, "chunk_index": i},
        )
        for i, fragment in enumerate(fragments)
    ]


def chunk_document(path: Path) -> list[Document]:
    """Point d'entrée : choisit la bonne stratégie selon source_type."""
    metadata, content = load_raw_document(path)
    source_type = metadata.get("source_type")

    strategies = {
        "faq": chunk_faq,
        "historical_ticket": chunk_ticket,
        "documentation": chunk_long_text,
        "guide": chunk_long_text,
    }

    strategy = strategies.get(source_type)
    if strategy is None:
        raise ValueError(
            f"source_type inconnu '{source_type}' dans {path.name}"
        )

    return strategy(metadata, content)