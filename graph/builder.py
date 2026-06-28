"""Construction of graphs"""

from langgraph.graph import START, END, StateGraph
from graph.edges import continue_to_retrieve, check_confidence
from graph.states import FactCheckState, InternalMapState, OutputMapState
from graph.nodes import (
    retrieve_evidence,
    judge_claim,
    ingest_claim,
    decompose_claim,
    aggregate_verdicts,
    format_output
)

# ---- Sub-Graph Costruction (fan-out) ----
subgraph_builder = StateGraph(
    state_schema=InternalMapState,
    output=OutputMapState
)

subgraph_builder.add_node(retrieve_evidence)
subgraph_builder.add_node(judge_claim)

subgraph_builder.add_edge(START, 'retrieve_evidence')
subgraph_builder.add_edge('retrieve_evidence', 'judge_claim')
subgraph_builder.add_edge('judge_claim', END)

subgraph = subgraph_builder.compile()


# ---- Main Graph Construction ----
main_builder = StateGraph(FactCheckState)

main_builder.add_node(ingest_claim)
main_builder.add_node(decompose_claim)
main_builder.add_node('sub_graph', subgraph)
main_builder.add_node(aggregate_verdicts)
main_builder.add_node(format_output)

main_builder.add_edge(START, 'ingest_claim')
main_builder.add_edge('ingest_claim', 'decompose_claim')
main_builder.add_conditional_edges('decompose_claim', continue_to_retrieve)
main_builder.add_conditional_edges('sub_graph', check_confidence)
main_builder.add_edge('aggregate_verdicts', 'format_output')
main_builder.add_edge('format_output', END)

main_graph = main_builder.compile()
