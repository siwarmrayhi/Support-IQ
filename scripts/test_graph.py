"""Teste le graphe complet avec validation d'ancrage."""

from supportiq.graph.workflow import graph


def run(ticket: str) -> None:
    result = graph.invoke({"ticket": ticket, "generation_attempts": 0})
    print(f"\nTicket     : {ticket}")
    print(f"Statut     : {result['status']}")
    print(f"Ancree     : {result['is_grounded']}")
    print(f"Tentatives : {result['generation_attempts']}")
    print(f"Reponse    : {result['answer']}")


if __name__ == "__main__":
    run("Mon paiement a échoué et mon abonnement vient d'être suspendu. Est-ce que mes projets sont conservés, et de combien de temps je dispose pour régulariser ?")