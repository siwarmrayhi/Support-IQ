"""Teste le graphe complet avec branchement conditionnel."""

from supportiq.graph.workflow import graph
import time



def run(ticket: str) -> None:
    result = graph.invoke({"ticket": ticket})
    print(f"\nTicket   : {ticket}")
    print(f"Statut   : {result['status']}")
    print(f"Pertinents : {[d.metadata.get('doc_id') for d in result['relevant_docs']]}")
    print(f"Reponse  : {result['answer']}")


if __name__ == "__main__":
    run("J'ai oublié mon mot de passe, comment le réinitialiser ?")
    run("Est-ce que CloudDesk propose un paiement échelonné en plusieurs mensualités ?")