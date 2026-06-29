"""Custom conditional edge function definitions"""

from typing import Literal
from graph.states import FactCheckState
from langgraph.types import Send

def continue_to_retrieve(state: FactCheckState) -> Literal['sub_graph']:
    """Spawn a sub-graph per sub-claim simultaneously"""
    
    return [Send('sub_graph', {'sub_claim': sub_claim, 'retry_count': 0}) for sub_claim in state['sub_claims']]


def check_confidence(state: FactCheckState) -> Literal['sub_graph', 'aggregate_verdicts']:
    """Check confidence scores of subclaims and retry for those under the threshold"""
    
    sub_claims = state['sub_claims']
    judge_results = state['judge_results']
    retry_count = state['retry_count']

    if retry_count <= 2:
        retries = [
            Send('sub_graph', {'sub_claim': list(result.keys())[0], 'retry_count': retry_count}) 
            for result in judge_results 
            if list(result.values())[0].confidence < 0.5
        ]
        if retries:
            return retries

    return 'aggregate_verdicts'