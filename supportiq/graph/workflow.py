"""Assemblage du graphe LangGraph : nodes et transitions."""

from langgraph.graph import END, START, StateGraph

from supportiq.graph.routing import route_after_grading
from supportiq.graph.state import SupportState
from supportiq.nodes.escalate import escalate
from supportiq.nodes.generate import generate_answer
from supportiq.nodes.grade import grade_documents
from supportiq.nodes.retrieve import retrieve

_builder = StateGraph(SupportState)

_builder.add_node("retrieve", retrieve)
_builder.add_node("grade_documents", grade_documents)
_builder.add_node("generate_answer", generate_answer)
_builder.add_node("escalate", escalate)

_builder.add_edge(START, "retrieve")
_builder.add_edge("retrieve", "grade_documents")

_builder.add_conditional_edges(
    "grade_documents",
    route_after_grading,
    ["generate_answer", "escalate"],
)

_builder.add_edge("generate_answer", END)
_builder.add_edge("escalate", END)

graph = _builder.compile()