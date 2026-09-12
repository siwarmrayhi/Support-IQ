"""Métriques d'évaluation du retrieval."""

from dataclasses import dataclass, field


@dataclass
class TicketResult:
    """Résultat du retrieval pour un seul ticket."""

    ticket_id: str
    expected_doc_ids: list[str]
    retrieved_doc_ids: list[str]
    has_exact_identifier: bool

    @property
    def found_doc_ids(self) -> list[str]:
        """Les documents attendus qui ont effectivement été retrouvés."""
        return [d for d in self.expected_doc_ids if d in self.retrieved_doc_ids]

    @property
    def is_full_hit(self) -> bool:
        """Vrai si TOUS les documents attendus ont été retrouvés."""
        return len(self.found_doc_ids) == len(self.expected_doc_ids)
    
    @property
    def reciprocal_rank(self) -> float:
        """1/rang du premier document attendu trouvé, 0 si absent."""
        for rank, doc_id in enumerate(self.retrieved_doc_ids, start=1):
            if doc_id in self.expected_doc_ids:
                return 1.0 / rank
        return 0.0


@dataclass
class EvalReport:
    """Agrégat de tous les résultats d'une évaluation."""

    results: list[TicketResult] = field(default_factory=list)

    def recall_at_k(self, subset: list[TicketResult] | None = None) -> float:
        """Proportion de documents attendus effectivement retrouvés."""
        items = subset if subset is not None else self.results
        total_expected = sum(len(r.expected_doc_ids) for r in items)
        total_found = sum(len(r.found_doc_ids) for r in items)
        if total_expected == 0:
            return float("nan")
        return total_found / total_expected
    
    def mrr(self, subset: list["TicketResult"] | None = None) -> float:
        """Moyenne des reciprocal_rank sur les tickets fournis."""
        items = subset if subset is not None else self.results
        if not items:
            return float("nan")
        return sum(r.reciprocal_rank for r in items) / len(items)

    @property
    def with_identifier(self) -> list[TicketResult]:
        return [r for r in self.results if r.has_exact_identifier]

    @property
    def without_identifier(self) -> list[TicketResult]:
        return [r for r in self.results if not r.has_exact_identifier]