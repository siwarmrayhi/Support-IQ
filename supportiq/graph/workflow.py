"""Assemblage du graphe LangGraph : nodes et transitions."""

from langgraph.graph import END, START, StateGraph

from supportiq.graph.state import SupportState
from supportiq.nodes.grade import grade_documents
from supportiq.nodes.retrieve import retrieve

_builder = StateGraph(SupportState)

_builder.add_node("retrieve", retrieve)
_builder.add_node("grade_documents", grade_documents)

_builder.add_edge(START, "retrieve")
_builder.add_edge("retrieve", "grade_documents")
_builder.add_edge("grade_documents", END)

graph = _builder.compile()