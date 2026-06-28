"""State Schema definitions"""

from typing import TypedDict, Annotated, Literal
import operator

from .reducer import overwrite_reducer

# Main Graph State
class FactCheckState(TypedDict):
    raw_claim : str
    sub_claims: list[str]
    verdict: Literal['supported', 'refuted', 'insufficient evidence']
    confidence: float
    retrieved_evidences: Annotated[list[str], operator.add]
    retry_count: Annotated[int, overwrite_reducer] # no reducer so it increases by one no matter how many nodes Send API calls 
    judge_results: Annotated[list[dict], operator.add]
    output: str

# Sub Graph States
class InternalMapState(TypedDict):
    sub_claim: str
    retrieved_evidences: list[str]
    judge_results: list[dict]
    retry_count: int

class OutputMapState(TypedDict):
    judge_results: list[dict]
    retry_count: int
    retrieved_evidences: list[str]