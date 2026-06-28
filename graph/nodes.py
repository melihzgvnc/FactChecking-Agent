"""Graph nodes definitions"""

from graph.states import FactCheckState, InternalMapState, OutputMapState
from model.decomposer import decomposer_model
from model.judge import judge_model
from prompts.prompts import DECOMPOSER_PROMPT, JUDGE_PROMPT
from retrieval.web_search import web_search


# ---- Sub-Graph Nodes ----

def retrieve_evidence(state: InternalMapState):
    """Search web and retrieve context regarding provided claim"""    

    sub_claim = state['sub_claim']

    search_results = web_search.invoke(sub_claim)['results']
    content = "\n".join([result['content'] for result in search_results])
    
    return {'retrieved_evidences': [content]}


def judge_claim(state: InternalMapState) -> OutputMapState:
    """Check claim against evidence and decide on verdict"""

    sub_claim = state['sub_claim']
    retrieved_evidences = state['retrieved_evidences']
    retry_count = state['retry_count'] + 1
    
    formatted_prompt = JUDGE_PROMPT.format(sub_claim=sub_claim, evidence=retrieved_evidences[0])
    input_msg = HumanMessage(content=formatted_prompt)
    
    response = judge_model.invoke([input_msg]) # returns verdict, confidence score and grounding sentence (ClaimCheck object)
    
    return {'judge_results': [{sub_claim: response}], 'retry_count': retry_count, 'retrieved_evidences': retrieved_evidences}


# ---- Main Graph Nodes -----

def ingest_claim(state: FactCheckState):
    
    raw_claim = state['raw_claim']
    normalized_claim = raw_claim.lower()

    return {'raw_claim': normalized_claim}


def decompose_claim(state: FactCheckState):

    claim = state['raw_claim']

    formatted_prompt = DECOMPOSER_PROMPT.format(raw_claim=claim)
    input_msg = HumanMessage(content=formatted_prompt)
    
    response = decomposer_model.invoke([input_msg])
    
    return {'sub_claims': response.sub_claims}


def aggregate_verdicts(state: FactCheckState):
    """Aggregate results into a single score"""

    judge_results = state['judge_results']

    sum_confidence = 0.0
    verdicts = []
    for result in judge_results:
        confidence = list(result.values())[0].confidence 
        sum_confidence += confidence / 100 if confidence > 1 else confidence
        subclaim_verdict = list(result.values())[0].verdict
        verdicts.append(subclaim_verdict)

    if 'refuted' in verdicts:
        overall_verdict = 'refuted'
    elif 'insufficient evidence' in verdicts:
        overall_verdict = 'insufficient evidence'
    else:
        overall_verdict = 'supported'
    
    overall_confidence = sum_confidence / len(judge_results)
    
    return {'verdict': overall_verdict, 'confidence': overall_confidence}


def format_output(state: FactCheckState):
    """Format output and present findings"""

    formatted_output = f"""For the given input, calculated results are as follows:\n
    Input: {state['raw_claim']}\n
    Verdict: {state['verdict']}\n
    Confidence: {state['confidence']}
    """

    return {'output': formatted_output}