"""Script temporaire : inspecte le decoupage d'un document donne."""

from pathlib import Path

from supportiq.rag.chunking import chunk_document

path = Path("data/raw/documentation/billing_subscription_plans.md")
chunks = chunk_document(path)

print(f"{len(chunks)} chunk(s) pour {path.name}\n")

for i, c in enumerate(chunks):
    print(f"--- chunk {i} ({len(c.page_content)} caracteres) ---")
    print(c.page_content)
    print()