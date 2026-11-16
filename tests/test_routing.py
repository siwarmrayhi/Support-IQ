from supportiq.graph.routing import (
    MAX_GENERATION_ATTEMPTS,
    route_after_grading,
    route_after_validation,
)


def test_aucun_document_pertinent_escalade():
    state = {"relevant_docs": []}
    assert route_after_grading(state) == "escalate"


def test_un_document_pertinent_genere_une_reponse():
    state = {"relevant_docs": ["un document"]}
    assert route_after_grading(state) == "generate_answer"


def test_reponse_fidele_va_a_la_decision():
    state = {"is_grounded": True, "generation_attempts": 1}
    assert route_after_validation(state) == "decide"


def test_reponse_non_fidele_au_premier_essai_est_regeneree():
    state = {"is_grounded": False, "generation_attempts": 1}
    assert route_after_validation(state) == "generate_answer"


def test_reponse_non_fidele_au_dernier_essai_abandonne():
    state = {"is_grounded": False, "generation_attempts": MAX_GENERATION_ATTEMPTS}
    assert route_after_validation(state) == "decide"