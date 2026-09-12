"""Teste le graphe minimal retrieve -> grade_documents."""

from supportiq.graph.workflow import graph

if __name__ == "__main__":
    result = graph.invoke({
    "ticket": "Mon paiement a échoué et mon abonnement vient d'être suspendu. Est-ce que mes projets sont conservés, et de combien de temps je dispose pour régulariser ?"
})

    print(f"Documents recuperes : {len(result['retrieved_docs'])}")
    print(f"Documents pertinents : {len(result['relevant_docs'])}")
    for doc in result["relevant_docs"]:
        print(f"  - {doc.metadata.get('doc_id')}")